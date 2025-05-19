"""
NLPを使用した個人情報検出のためのユーティリティモジュール
"""
import spacy
from collections import defaultdict
import re
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    # spaCyの日本語モデルをロード
    nlp = spacy.load('ja_core_news_md')
    logger.info("spaCyの日本語モデルを正常にロードしました。")
except Exception as e:
    logger.error(f"spaCyモデルのロードに失敗しました: {e}")
    logger.warning("NLP機能は制限されます。")
    nlp = None

def extract_named_entities(text):
    """
    入力テキストから固有表現を抽出する

    Args:
        text (str): 入力テキスト

    Returns:
        dict: エンティティのタイプとテキストのリスト
    """
    if not nlp:
        logger.warning("NLPモデルが利用できないため、固有表現抽出はスキップされます。")
        return {}

    try:
        doc = nlp(text)
        entities = defaultdict(list)

        # 固有表現を抽出
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)

        # 人名を検出（PERSON以外の方法でも）
        for token in doc:
            if token.pos_ == 'PROPN' and len(token.text) >= 2:
                if token.text not in [e for ent_list in entities.values() for e in ent_list]:
                    entities['PERSON_CANDIDATE'].append(token.text)

        # 企業名の候補を検出（名詞の連続で、数字を含まない）
        company_names = []
        for chunk in doc.noun_chunks:
            if len(chunk.text) >= 3 and not re.search(r'\d', chunk.text):
                if chunk.text not in [e for ent_list in entities.values() for e in ent_list]:
                    company_names.append(chunk.text)

        if company_names:
            entities['ORGANIZATION_CANDIDATE'] = company_names

        return dict(entities)
    except Exception as e:
        logger.error(f"固有表現抽出に失敗しました: {e}")
        return {}

def detect_personal_info_with_nlp(text):
    """
    NLPを使用して個人情報を検出する

    Args:
        text (str): 入力テキスト

    Returns:
        dict: タイプごとの個人情報のリスト
    """
    entities = extract_named_entities(text)
    personal_info = {}

    # 人名
    if 'PERSON' in entities:
        personal_info['name'] = entities['PERSON']

    if 'PERSON_CANDIDATE' in entities:
        if 'name' not in personal_info:
            personal_info['name'] = []
        personal_info['name'].extend(entities['PERSON_CANDIDATE'])

    # 組織名・企業名
    if 'ORG' in entities:
        personal_info['company'] = entities['ORG']

    if 'ORGANIZATION_CANDIDATE' in entities:
        if 'company' not in personal_info:
            personal_info['company'] = []
        personal_info['company'].extend(entities['ORGANIZATION_CANDIDATE'])

    # 住所・場所
    if 'LOC' in entities or 'GPE' in entities:
        personal_info['address'] = []
        if 'LOC' in entities:
            personal_info['address'].extend(entities['LOC'])
        if 'GPE' in entities:
            personal_info['address'].extend(entities['GPE'])

    # 日付と生年月日を区別
    if 'DATE' in entities:
        dates = entities['DATE']
        birthdates = []
        normal_dates = []

        # 生年月日の文脈を含む日付を判別
        from .patterns import BIRTHDAY_CONTEXT
        import re
        birthday_context_pattern = re.compile(BIRTHDAY_CONTEXT)

        for date in dates:
            # 前後30文字の範囲を調べて生年月日かどうか判定
            date_pos = text.find(date)
            if date_pos >= 0:
                start_pos = max(0, date_pos - 30)
                end_pos = min(len(text), date_pos + len(date) + 30)
                context = text[start_pos:end_pos]

                if birthday_context_pattern.search(context):
                    birthdates.append(date)
                else:
                    normal_dates.append(date)

        if birthdates:
            personal_info['birthdate'] = birthdates

        if normal_dates:
            personal_info['date'] = normal_dates

    return personal_info