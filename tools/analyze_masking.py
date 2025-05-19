#!/usr/bin/env python3
"""
マスキング結果の詳細分析スクリプト
"""
import sys
import pandas as pd
import json
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_masking(csv_file):
    """
    マスキング結果の詳細分析

    Args:
        csv_file (str): マスキング済みCSVファイルのパス
    """
    print(f"ファイル '{csv_file}' の分析を実行します\n")

    # CSVファイルの読み込み
    df = pd.read_csv(csv_file)

    # 各行ごとに詳細分析
    for _, row in df.iterrows():
        print("-" * 80)
        print(f"ID: {row['id']} - カテゴリ: {row['problem_category']}")
        print(f"顧客名: {row['customer_name']}")

        # オリジナルテキスト
        print("\n【元のテキスト】")
        print(row['inquiry_text'])

        # マスキング後テキスト
        print("\n【マスキング後】")
        print(row['masked_inquiry'])

        # マスキング項目の詳細
        print("\n【マスキング項目】")
        if row['masked_items']:
            masked_items = row['masked_items'].split(',')
            for item in masked_items:
                if ':' in item:
                    item_type, content = item.split(':', 1)
                    print(f"- {item_type}: {content}")
                else:
                    print(f"- {item}")

        # マスキングカウント
        print("\n【マスキングカウント】")
        if row['mask_count']:
            for count_info in row['mask_count'].split(','):
                print(f"- {count_info}")

        print("\n")

if __name__ == "__main__":
    # マスキング結果ファイルのパス（相対パス）
    current_dir = Path(__file__).parent.parent  # プロジェクトのルートディレクトリ
    masked_file = current_dir / "data" / "output" / "advanced_test_data_masked.csv"

    # 分析実行
    analyze_masking(masked_file)
