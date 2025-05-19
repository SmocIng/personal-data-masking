"""
個人情報のマスキング処理を行うモジュール
"""
import re
import logging
from .patterns import PATTERNS, MASK_REPLACEMENTS
from .nlp_utils import detect_personal_info_with_nlp

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersonalInfoMasker:
    """
    個人情報マスキングを行うクラス
    """

    def __init__(self, use_nlp=True):
        """
        初期化

        Args:
            use_nlp (bool): NLPを使用するかどうか
        """
        self.use_nlp = use_nlp
        self.patterns = PATTERNS
        self.replacements = MASK_REPLACEMENTS
        logger.info(f"PersonalInfoMasker を初期化しました。NLP使用: {use_nlp}")

    def _mask_with_regex(self, text):
        """
        正規表現で個人情報をマスキングする

        Args:
            text (str): 入力テキスト

        Returns:
            tuple: (マスキングしたテキスト, マスキングした情報のリスト)
        """
        masked_text = text
        masked_items = []

        # 検出結果を格納する配列（位置情報を保持するため）
        detection_results = []

        # 各パターンで検索して検出結果を収集
        for pattern_type, pattern in self.patterns.items():
            matches = list(pattern.finditer(text))  # 元のテキストで検索

            for match in matches:
                start, end = match.span()
                original_text = match.group(0)

                # 特殊ケース：birthdateが検出された場合はdateと重複しないように
                if pattern_type == 'birthdate':
                    detection_results.append({
                        'start': start,
                        'end': end,
                        'type': pattern_type,
                        'text': original_text,
                        'priority': 1  # birthdateは優先度高
                    })
                else:
                    detection_results.append({
                        'start': start,
                        'end': end,
                        'type': pattern_type,
                        'text': original_text,
                        'priority': 2  # その他は通常優先度
                    })

        # 優先度が高く、範囲が広い検出結果を優先するためにソート
        detection_results.sort(key=lambda x: (x['priority'], -(x['end'] - x['start'])))

        # 重複を除外するための処理
        processed_ranges = []
        final_detections = []

        for result in detection_results:
            # この範囲が既に処理済みの範囲と重複するかチェック
            is_overlapping = False
            for proc_start, proc_end in processed_ranges:
                # 完全包含または部分重複の場合
                if not (result['end'] <= proc_start or result['start'] >= proc_end):
                    is_overlapping = True
                    break

            # 重複していなければ処理対象に追加
            if not is_overlapping:
                processed_ranges.append((result['start'], result['end']))
                final_detections.append(result)

        # 後ろから処理して置換のずれを防ぐ
        final_detections.sort(key=lambda x: x['start'], reverse=True)

        for detection in final_detections:
            pattern_type = detection['type']
            original_text = detection['text']
            start = detection['start']
            end = detection['end']

            replacement = self.replacements[pattern_type]

            # マスキング対象を記録
            masked_item = f"{pattern_type}:{original_text}"
            masked_items.append(masked_item)

            # テキストを置換
            masked_text = masked_text[:start] + replacement + masked_text[end:]

        return masked_text, masked_items

    def _mask_with_nlp(self, text, already_masked_text):
        """
        NLPを使って個人情報をマスキングする

        Args:
            text (str): 元の入力テキスト
            already_masked_text (str): 正規表現でマスク済みのテキスト

        Returns:
            tuple: (マスキングしたテキスト, マスキングした情報のリスト)
        """
        masked_text = already_masked_text
        masked_items = []

        # NLPで個人情報を検出
        nlp_entities = detect_personal_info_with_nlp(text)

        if not nlp_entities:
            return masked_text, masked_items

        # 検出した各タイプに対応
        for entity_type, entities in nlp_entities.items():
            replacement_key = self._map_entity_type_to_replacement(entity_type)
            replacement = self.replacements.get(replacement_key)

            if not replacement:
                continue

            for entity in entities:
                # 既にマスキングされていない場合のみ処理
                if entity in masked_text:
                    # エンティティが複数回出現する可能性があるため、
                    # 元のテキストでの位置を特定してから置換
                    entity_escaped = re.escape(entity)
                    masked_text = re.sub(f"(?<![\\w]){entity_escaped}(?![\\w])", replacement, masked_text)
                    masked_items.append(f"{replacement_key}:{entity}")

        return masked_text, masked_items

    def _map_entity_type_to_replacement(self, entity_type):
        """
        NLPのエンティティタイプをマスキングタイプにマッピングする

        Args:
            entity_type (str): エンティティタイプ

        Returns:
            str: マスキングタイプ
        """
        mapping = {
            'name': 'name',
            'PERSON': 'name',
            'PERSON_CANDIDATE': 'name',
            'company': 'company',
            'ORG': 'company',
            'ORGANIZATION_CANDIDATE': 'company',
            'address': 'address',
            'LOC': 'address',
            'GPE': 'address',
            'date': 'date',          # 一般的な日付
            'DATE': 'date',          # 一般的な日付
            'birthdate': 'birthdate', # 生年月日
            'phone': 'phone',
            'email': 'email'
        }

        return mapping.get(entity_type, 'unknown')

    def mask_personal_info(self, text):
        """
        テキスト内の個人情報をマスキングする

        Args:
            text (str): 入力テキスト

        Returns:
            tuple: (マスキングしたテキスト, マスキングした情報のリスト)
        """
        if not text or not isinstance(text, str):
            return "", []

        # まず正規表現でマスキング
        masked_text, masked_items = self._mask_with_regex(text)

        # NLP使用が有効な場合、追加でマスキング
        if self.use_nlp:
            masked_text, nlp_masked_items = self._mask_with_nlp(text, masked_text)
            masked_items.extend(nlp_masked_items)

        # マスキング後の後処理

        # 1. 二重括弧の問題を修正 - 正規表現で[[内容]]を[内容]に変換
        double_bracket_pattern = re.compile(r'\[\[([^\]]+)\]\]')
        while double_bracket_pattern.search(masked_text):
            masked_text = double_bracket_pattern.sub(r'[\1]', masked_text)

        # 2. 連続したマスキング表記を一つにまとめる
        for replacement in self.replacements.values():
            repeated_pattern = re.compile(f'({re.escape(replacement)})+')
            masked_text = repeated_pattern.sub(replacement, masked_text)

        # 3. 一部が不自然に切れている場合に対応
        # 「生年月日」関連キーワードが「企業情報」としてマスキングされる問題の修正
        birth_keywords = ['生年月日', '誕生日', '生まれ', '出生']

        # 「生年月日」タイプのマスキングがあるか確認
        has_birthdate = any(item.startswith('birthdate:') for item in masked_items)

        # 企業情報マスキングの修正
        company_items = []
        for i, item in enumerate(masked_items):
            if item.startswith('company:'):
                # 生年月日関連キーワードを含む企業情報は修正
                if any(keyword in item for keyword in birth_keywords):
                    company_items.append((i, item))

        # 「company:生年月日」のようなマスキング項目を削除
        if company_items:
            for idx, _ in reversed(company_items):
                masked_items.pop(idx)

        # 生年月日が企業情報としてマスキングされている場合、置き換える
        if has_birthdate:
            # 生年月日マスキングが存在する場合、企業情報マスキングを生年月日に置き換え
            for keyword in birth_keywords:
                if "[企業情報]" in masked_text and keyword in text:
                    masked_text = masked_text.replace("[企業情報]", "[生年月日]")
                    break

        # 不自然な切れ目の修正 - 「氏名」の後ろがおかしい場合
        name_endings = re.findall(r'\[氏名\]([^\s\.,?!。、．？！]{1,2})', masked_text)
        for ending in name_endings:
            if ending not in ["の", "が", "を", "に", "は", "も", "で", "と", "へ", "や", "か", "な", "ね", "よ", "ね"]:
                masked_text = masked_text.replace(f'[氏名]{ending}', '[氏名]')

        # 文末での不自然な切れ目修正（文末が「です」「ます」で終わるケース）
        masked_text = re.sub(r'\[氏名\]([すでま]{1,2})。', r'[氏名]。', masked_text)

        # 不自然な切れ目の修正 - 「企業情報」の後ろがおかしい場合
        company_endings = re.findall(r'\[企業情報\]([^\s\.,?!。、．？！]{1,3})', masked_text)
        for ending in company_endings:
            if len(ending) <= 2 and ending not in ["の", "が", "を", "に", "は", "も", "で", "と", "へ", "や", "か", "な", "ね", "よ"]:
                masked_text = masked_text.replace(f'[企業情報]{ending}', '[企業情報]')

        # 4. 整形：空白の連続を一つにまとめる
        masked_text = re.sub(r'\s+', ' ', masked_text)

        # 5. マスキング対象が空になっていないか確認
        if len(masked_items) > 0 and len(masked_text.strip()) == 0:
            logger.warning("マスキング処理後にテキストが空になりました。元テキスト長: %d", len(text))
            # 最低限の内容を残す
            masked_text = "[全文がマスキング対象]"

        return masked_text, masked_items