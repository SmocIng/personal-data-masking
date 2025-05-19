#!/usr/bin/env python3
"""
大規模なテストデータを生成するスクリプト
"""
import sys
import pandas as pd
import numpy as np
import random
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 名前のリスト
first_names = [
    "太郎", "花子", "一郎", "直子", "健太", "美香", "次郎", "裕子", "大輔", "真理",
    "光", "恵", "浩二", "由美子", "修", "舞", "武", "彩", "誠", "香織"
]

last_names = [
    "佐藤", "鈴木", "高橋", "田中", "伊藤", "渡辺", "山本", "中村", "小林", "加藤",
    "吉田", "山田", "佐々木", "山口", "松本", "井上", "木村", "林", "清水", "山崎"
]

# 電話番号のリスト（架空の番号）
phone_formats = [
    "03-XXXX-XXXX",
    "06-XXXX-XXXX",
    "070-XXXX-XXXX",
    "080-XXXX-XXXX",
    "090-XXXX-XXXX"
]

# メールアドレスのリスト（架空のアドレス）
email_domains = [
    "example.com", "test.co.jp", "sample.jp", "mail.com", "mymail.jp", "dummy.org"
]

# 企業名のリスト
companies = [
    "テスト株式会社", "サンプル商事", "データ分析株式会社", "モデル開発有限会社", "テクノロジー株式会社",
    "デジタルソリューションズ", "ITサービス株式会社", "システム開発", "クラウドコンピューティング", "情報処理株式会社"
]

# 都道府県のリスト（一部）
prefectures = [
    "東京都", "大阪府", "神奈川県", "愛知県", "埼玉県", "千葉県", "兵庫県", "福岡県", "北海道", "京都府"
]

# 市区町村のリスト（一部）
cities = [
    "千代田区", "中央区", "港区", "新宿区", "渋谷区",
    "大阪市", "名古屋市", "横浜市", "札幌市", "福岡市"
]

# 問い合わせ内容のテンプレート
inquiry_templates = [
    "{name}と申します。{company}で勤務しております。御社の製品について問い合わせがあります。連絡先は{phone}、メールは{email}です。",
    "{name}です。生年月日は{birthdate}です。アカウント情報の更新をしたいです。電話番号は{phone}に変更してください。",
    "{company}の{name}と申します。{address}にある事務所で製品を使用していますが、問題が発生しています。至急{phone}に連絡をお願いします。",
    "はじめまして、{name}です。{date}に注文した商品がまだ届きません。住所は{address}です。メールアドレスは{email}です。",
    "{name}と言います。{company}への転職を検討しています。{birthdate}生まれの{age}歳です。連絡先は{email}か{phone}にお願いします。",
    "{company}の件でお問い合わせします。担当者の{name}様へ連絡がつかず困っています。{date}の打ち合わせについて確認したいです。",
    "私は{name}、{birthdate}生まれです。{address}に住んでいます。{date}に予約した件について確認したいです。連絡は{phone}までお願いします。",
    "{name}です。{company}で{date}に開催されるイベントに参加を希望します。詳細は{email}に送ってください。",
    "{address}に住んでいる{name}です。{company}の製品を購入しましたが、不具合があります。生年月日は{birthdate}です。電話は{phone}です。",
    "{name}と申します。{date}に御社でお買い物をしました。返品したいのですが、手続きを教えてください。住所は{address}、メールは{email}です。"
]

def generate_random_phone():
    """
    ランダムな電話番号を生成する
    """
    format = random.choice(phone_formats)
    phone = ""
    for c in format:
        if c == "X":
            phone += str(random.randint(0, 9))
        else:
            phone += c
    return phone

def generate_random_email(name):
    """
    ランダムなメールアドレスを生成する
    """
    domain = random.choice(email_domains)
    name_part = name.lower().replace(" ", ".").replace("　", ".")

    # ランダムに数字を追加
    if random.random() > 0.5:
        name_part += str(random.randint(1, 999))

    return f"{name_part}@{domain}"

def generate_random_address():
    """
    ランダムな住所を生成する
    """
    prefecture = random.choice(prefectures)
    city = random.choice(cities)
    chome = f"{random.randint(1, 10)}-{random.randint(1, 20)}-{random.randint(1, 15)}"
    return f"{prefecture}{city}{chome}"

def generate_random_date():
    """
    ランダムな日付を生成する (2023-2025年)
    """
    year = random.randint(2023, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 簡易化のため28日まで

    # 日付表記のバリエーション
    formats = [
        f"{year}年{month}月{day}日",
        f"{year}/{month}/{day}",
        f"{year}-{month}-{day}"
    ]

    return random.choice(formats)

def generate_random_birthdate():
    """
    ランダムな生年月日を生成する (1960-2000年)
    """
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 簡易化のため28日まで

    # 日付表記のバリエーション
    formats = [
        f"{year}年{month}月{day}日",
        f"{year}/{month}/{day}",
        f"{year}-{month}-{day}"
    ]

    return random.choice(formats)

def generate_large_test_data(num_records=50, output_file=None):
    """
    大規模なテストデータを生成する

    Args:
        num_records (int): 生成するレコード数
        output_file (str): 出力ファイルパス

    Returns:
        pd.DataFrame: 生成したデータフレーム
    """
    # データを格納するリスト
    data = []

    # レコードを生成
    for i in range(1, num_records + 1):
        # 名前を生成
        last_name = random.choice(last_names)
        first_name = random.choice(first_names)
        full_name = f"{last_name} {first_name}"

        # 問い合わせカテゴリ
        categories = ["アカウント", "商品", "決済", "返品", "サービス", "技術サポート", "その他"]
        category = random.choice(categories)

        # 電話番号を生成
        phone = generate_random_phone()

        # メールアドレスを生成
        email = generate_random_email(full_name)

        # 企業名を生成
        company = random.choice(companies)

        # 住所を生成
        address = generate_random_address()

        # 日付を生成
        date = generate_random_date()

        # 生年月日を生成
        birthdate = generate_random_birthdate()
        age = 2025 - int(birthdate.split("年")[0] if "年" in birthdate else birthdate.split("/")[0].split("-")[0])

        # テンプレートを選択して問い合わせ文を生成
        template = random.choice(inquiry_templates)
        inquiry_text = template.format(
            name=full_name,
            phone=phone,
            email=email,
            company=company,
            address=address,
            date=date,
            birthdate=birthdate,
            age=age
        )

        # 対応状況をランダムに選択
        status = random.choice(["対応済み", "対応中", "未対応"])

        # データに追加
        data.append({
            "id": i,
            "problem_category": category,
            "customer_name": full_name,
            "inquiry_text": inquiry_text,
            "response_status": status
        })

    # データフレームを作成
    df = pd.DataFrame(data)

    # ファイルに出力
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"{num_records}件のテストデータを '{output_file}' に出力しました。")

    return df

if __name__ == "__main__":
    # 出力ファイルのパス（相対パス）
    current_dir = Path(__file__).parent.parent  # プロジェクトのルートディレクトリ
    output_path = current_dir / "tests" / "large_test_data.csv"

    # 100件のテストデータを生成
    generate_large_test_data(100, output_path)
