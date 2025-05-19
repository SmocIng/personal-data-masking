# 改善点のテスト用スクリプト
import sys
import os
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.masking import PersonalInfoMasker

def test_improved_masking():
    masker = PersonalInfoMasker(use_nlp=True)

    # テストケース1: 二重括弧問題のテスト
    text1 = "私はテスト株式会社株式会社に勤めています。"
    masked1, items1 = masker.mask_personal_info(text1)
    print(f"元テキスト: {text1}")
    print(f"マスキング後: {masked1}")
    print(f"マスキング項目: {items1}\n")

    # テストケース2: 生年月日と日付の区別テスト
    text2 = "生年月日は1990年5月10日です。次回の面談は2025年6月20日に予定しています。"
    masked2, items2 = masker.mask_personal_info(text2)
    print(f"元テキスト: {text2}")
    print(f"マスキング後: {masked2}")
    print(f"マスキング項目: {items2}\n")

    # テストケース3: 「〜と申します」などの表現対応
    text3 = "山田太郎と申します。佐藤花子と言います。私は鈴木一郎です。"
    masked3, items3 = masker.mask_personal_info(text3)
    print(f"元テキスト: {text3}")
    print(f"マスキング後: {masked3}")
    print(f"マスキング項目: {items3}\n")

    # テストケース4: マスキング後のテキスト整合性テスト
    text4 = "株式会社テクノロジー 山田太郎 連絡先: 090-1234-5678 生年月日:1985年4月1日"
    masked4, items4 = masker.mask_personal_info(text4)
    print(f"元テキスト: {text4}")
    print(f"マスキング後: {masked4}")
    print(f"マスキング項目: {items4}")

if __name__ == "__main__":
    test_improved_masking()
