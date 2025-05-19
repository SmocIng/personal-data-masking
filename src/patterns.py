"""
個人情報を検出するための正規表現パターン定義
"""
import re

# 氏名（日本語）のパターン - 氏名と敬称（様、さん等）を含む、「〜と申します」などの表現も対応
NAME_PATTERN = r'(?:'
NAME_PATTERN += r'[一-龯々ぁ-んァ-ヶー]{1,5}[　 ][一-龯々ぁ-んァ-ヶー]{1,5}(?:と申します|です|と言います)?|'  # 姓名 + 定型表現
NAME_PATTERN += r'[一-龯々ぁ-んァ-ヶー]{1,5}(?:さん|様|君|くん|ちゃん|先生)|'  # 姓/名 + 敬称
NAME_PATTERN += r'(?:私は|わたしは|僕は|ぼくは|俺は|おれは|わたくしは)[　 ]*[一-龯々ぁ-んァ-ヶー]{1,5}(?:[　 ][一-龯々ぁ-んァ-ヶー]{1,5})?|'  # 「私は〜」で始まる自己紹介
NAME_PATTERN += r'[一-龯々ぁ-んァ-ヶー]{1,5}[　 ]?[一-龯々ぁ-んァ-ヶー]{1,5}[　 ]?(?:と申します|です|と言います)'  # 姓名 + 定型表現（スペースなしも対応）
NAME_PATTERN += r')'

# 電話番号のパターン（ハイフンあり・なし両対応）
PHONE_PATTERN = r'(?:0\d{1,4}-\d{1,4}-\d{4}|0\d{9,10})'

# 生年月日のパターン
# YYYY/MM/DD, YYYY年MM月DD日, YYYY-MM-DD 等の形式に対応
# 生年月日を示す文脈の単語を含むパターンも定義
BIRTHDAY_CONTEXT = r'(?:生年月日|誕生日|生まれ|生れ|出生|誕生)'
DATE_PATTERN = r'(?:\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)'

# 生年月日コンテキスト付きの日付パターン（前後に生年月日を示す表現がある場合）
BIRTHDATE_WITH_CONTEXT_PATTERN = rf'(?:{BIRTHDAY_CONTEXT}.{{0,10}}{DATE_PATTERN}|{DATE_PATTERN}.{{0,10}}{BIRTHDAY_CONTEXT})'

# メールアドレスのパターン
EMAIL_PATTERN = r'(?:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'

# 住所のパターン（都道府県・市区町村から始まるパターンに対応）
# 都道府県名のリスト
PREFECTURE_NAMES = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
    '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
    '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
    '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
]

# よくある市の名前（一部）
COMMON_CITIES = [
    '札幌市', '仙台市', 'さいたま市', '千葉市', '横浜市', '川崎市', '相模原市',
    '新潟市', '静岡市', '浜松市', '名古屋市', '京都市', '大阪市', '堺市', '神戸市',
    '岡山市', '広島市', '北九州市', '福岡市', '熊本市'
]

# 住所パターン（都道府県または市から始まり、数字と方角を含む可能性がある）
ADDRESS_PREFIX_PATTERN = '|'.join([re.escape(name) for name in (PREFECTURE_NAMES + COMMON_CITIES)])
ADDRESS_PATTERN = rf'(?:({ADDRESS_PREFIX_PATTERN})[\s]*.+?(?:[0-9０-９]+[^0-9０-９\s]{1,3}|丁目|番地|号))'

# 企業情報・職務経歴のパターン
COMPANY_SUFFIX = '株式会社|有限会社|合同会社|社団法人|財団法人|株式会社|㈱|（株）|\\(株\\)|LLC|Co\\.|Corp\\.|Inc\\.'
COMPANY_PATTERN = rf'(?:[ァ-ヶー一-龯々A-Za-z]+{COMPANY_SUFFIX}|{COMPANY_SUFFIX}[ァ-ヶー一-龯々A-Za-z]+)'

# コンパイル済みの正規表現パターン
PATTERNS = {
    'name': re.compile(NAME_PATTERN),
    'phone': re.compile(PHONE_PATTERN),
    'birthdate': re.compile(BIRTHDATE_WITH_CONTEXT_PATTERN),  # 生年月日コンテキスト付き
    'date': re.compile(DATE_PATTERN),  # 一般的な日付
    'email': re.compile(EMAIL_PATTERN),
    'address': re.compile(ADDRESS_PATTERN),
    'company': re.compile(COMPANY_PATTERN)
}

# マスキング後の置換文字列
MASK_REPLACEMENTS = {
    'name': '[氏名]',
    'phone': '[電話番号]',
    'date': '[生年月日]',
    'email': '[メールアドレス]',
    'address': '[住所]',
    'company': '[企業情報]'
}

# 全パターンをまとめた大きな正規表現（順番が重要）
ALL_PATTERNS_DICT = {
    'name': (NAME_PATTERN, '[氏名]'),
    'phone': (PHONE_PATTERN, '[電話番号]'),
    'birthdate': (BIRTHDATE_WITH_CONTEXT_PATTERN, '[生年月日]'),
    'date': (DATE_PATTERN, '[日付]'),
    'email': (EMAIL_PATTERN, '[メールアドレス]'),
    'address': (ADDRESS_PATTERN, '[住所]'),
    'company': (COMPANY_PATTERN, '[企業情報]')
}

# マスキング後の置換文字列
MASK_REPLACEMENTS = {
    'name': '[氏名]',
    'phone': '[電話番号]',
    'birthdate': '[生年月日]',
    'date': '[日付]',
    'email': '[メールアドレス]',
    'address': '[住所]',
    'company': '[企業情報]'
}

# 全パターンをまとめた大きな正規表現（順番が重要）
ALL_PATTERNS_DICT = {
    'name': (NAME_PATTERN, '[氏名]'),
    'phone': (PHONE_PATTERN, '[電話番号]'),
    'date': (DATE_PATTERN, '[生年月日]'),
    'email': (EMAIL_PATTERN, '[メールアドレス]'),
    'address': (ADDRESS_PATTERN, '[住所]'),
    'company': (COMPANY_PATTERN, '[企業情報]')
}