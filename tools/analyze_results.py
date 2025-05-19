#!/usr/bin/env python3
"""
マスキング結果の集計分析
"""
import sys
import pandas as pd
import os
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_mask_counts(csv_file):
    """
    マスキング結果のカウントを分析する
    """
    print(f"ファイル '{csv_file}' のマスキング結果を分析します\n")

    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # mask_countを解析
    mask_counts = [item.split(',') for item in df['mask_count']]

    # 合計マスキング数を集計
    total_counts = [int(item.split(':')[1]) for item in [items[-1] for items in mask_counts]]

    # 基本統計情報を表示
    print(f"合計マスキング数: {sum(total_counts)}件")
    print(f"平均マスキング数/レコード: {sum(total_counts)/len(total_counts):.2f}件")
    print(f"最小マスキング数: {min(total_counts)}件")
    print(f"最大マスキング数: {max(total_counts)}件")

    # タイプ別のマスキング数
    print("\nマスキングタイプ別の総数:")
    types = ['name', 'phone', 'date', 'email', 'address', 'company', 'birthdate']
    type_counts = {}

    for t in types:
        counts = [int(item.split(':')[1]) for items in mask_counts for item in items if item.startswith(f'{t}:')]
        if counts:
            type_counts[t] = sum(counts)
            print(f"- {t}: {sum(counts)}件 ({sum(counts)/sum(total_counts)*100:.1f}%)")
        else:
            type_counts[t] = 0
            print(f"- {t}: 0件 (0.0%)")

    # マスキング前後の平均文字数変化
    avg_orig_len = df['inquiry_text'].str.len().mean()
    avg_masked_len = df['masked_inquiry'].str.len().mean()
    print(f"\n文字数の変化:")
    print(f"- マスキング前の平均文字数: {avg_orig_len:.1f}文字")
    print(f"- マスキング後の平均文字数: {avg_masked_len:.1f}文字")
    print(f"- 変化率: {(avg_masked_len/avg_orig_len - 1)*100:.1f}%")

    # マスキング後のテキストに特定のパターンが含まれる件数
    print("\n検出パターン:")
    patterns = {
        "二重括弧": "\\[\\[",  # [[
        "連続マスキング": "\\]\\[",  # ][
        "不自然な切れ目": "\\][a-zA-Z0-9ぁ-んァ-ヶ一-龯々]{1,2}[。、．,.!?]"  # ]X。
    }

    for name, pattern in patterns.items():
        count = df['masked_inquiry'].str.contains(pattern).sum()
        print(f"- {name}: {count}件 ({count/len(df)*100:.1f}%)")

    print("\n分析が完了しました。")

if __name__ == "__main__":
    # 分析するファイル
    csv_file = "data/output/large_test_data_masked.csv"

    # 分析を実行
    analyze_mask_counts(csv_file)
