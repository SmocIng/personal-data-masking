#!/usr/bin/env python3
"""
個人情報マスキング処理を実行するスクリプト
"""
import sys
import os
import argparse
import logging
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# プロジェクトのルートディレクトリをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.masking import PersonalInfoMasker
from src.counter import count_masked_info, format_count_result

# ロガーの設定
# 以前の設定をリセット
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# ログディレクトリが存在しない場合は作成
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# ログファイルのパス
log_path = log_dir / 'masking.log'

# コンソール出力ハンドラ
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# ファイル出力ハンドラ
file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# フォーマッタ
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# rootロガーにハンドラを追加
logging.root.setLevel(logging.INFO)
logging.root.addHandler(console_handler)
logging.root.addHandler(file_handler)

# このモジュール用のロガーを取得
logger = logging.getLogger(__name__)

def process_csv(input_file, output_file, inquiry_column, use_nlp=True):
    """
    CSVファイルを処理して個人情報をマスキングする

    Args:
        input_file (str): 入力CSVファイルパス
        output_file (str): 出力CSVファイルパス
        inquiry_column (str): 問い合わせ文のカラム名
        use_nlp (bool): NLPを使用するかどうか

    Returns:
        bool: 処理成功したかどうか
    """
    try:
        # CSVファイルを読み込み
        logger.info(f"CSVファイル '{input_file}' を読み込んでいます...")
        df = pd.read_csv(input_file)

        if inquiry_column not in df.columns:
            logger.error(f"指定されたカラム '{inquiry_column}' がCSVファイルに存在しません。")
            return False

        # マスキング処理のインスタンスを作成
        masker = PersonalInfoMasker(use_nlp=use_nlp)

        # マスキング結果を格納するカラムを追加
        df['masked_inquiry'] = ""
        df['masked_items'] = ""
        df['mask_count'] = ""

        # 各行を処理
        logger.info("マスキング処理を実行中...")
        for i, row in tqdm(df.iterrows(), total=len(df), desc="マスキング処理"):
            # 問い合わせ文を取得
            inquiry_text = row[inquiry_column]

            # マスキング処理を実行
            if pd.notna(inquiry_text) and isinstance(inquiry_text, str):
                masked_text, masked_items = masker.mask_personal_info(inquiry_text)

                # マスキング項目をカンマ区切りの文字列に変換
                masked_items_str = ",".join(masked_items) if masked_items else ""

                # マスキングカウントを算出
                count_result = count_masked_info(masked_items)
                count_str = format_count_result(count_result)

                # 結果をデータフレームに格納
                df.at[i, 'masked_inquiry'] = masked_text
                df.at[i, 'masked_items'] = masked_items_str
                df.at[i, 'mask_count'] = count_str
            else:
                df.at[i, 'masked_inquiry'] = ""
                df.at[i, 'masked_items'] = ""
                df.at[i, 'mask_count'] = ""

        # 出力ディレクトリが存在しない場合は作成
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 処理結果をCSVに出力
        logger.info(f"処理結果を '{output_file}' に出力しています...")
        df.to_csv(output_file, index=False)

        logger.info(f"処理が完了しました。合計 {len(df)} 件のデータを処理しました。")
        return True

    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {str(e)}", exc_info=True)
        return False

def main():
    """
    メイン処理
    """
    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(description='個人情報マスキングプログラム')
    parser.add_argument('-i', '--input', required=True, help='入力CSVファイルパス')
    parser.add_argument('-o', '--output', help='出力CSVファイルパス（省略時は自動生成）')
    parser.add_argument('-c', '--column', required=True, help='問い合わせ文のカラム名')
    parser.add_argument('--no-nlp', action='store_true', help='NLP処理を使用しない')

    args = parser.parse_args()

    # 入出力ファイルのパスを設定
    input_file = args.input
    if not args.output:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_masked{input_path.suffix}")
    else:
        output_file = args.output

    # 処理の実行
    success = process_csv(input_file, output_file, args.column, not args.no_nlp)

    # 終了コードを設定
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
