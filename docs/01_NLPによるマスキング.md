# 個人情報マスキングプログラム

## 1. 概要
toCサービスにおけるカスタマーサポートの問い合わせ文から個人情報をマスキングするためのテキストクレンジングプログラムです。
マスキングした個人情報は別カラムに保持し、データ分析などの目的で必要に応じて参照できます。

## 2. マスキング対象
以下の個人情報をマスキング対象とします：
- 氏名（日本語）：`[氏名]`に置換
- 電話番号：`[電話番号]`に置換
- 生年月日：`[生年月日]`に置換
- 住所：`[住所]`に置換
- 企業情報・職務経歴：`[企業情報]`に置換
- メールアドレス：`[メールアドレス]`に置換

## 3. 処理フロー
1. 問い合わせ文を入力として受け取る
2. 正規表現とNLPを用いて個人情報を検出
3. 検出した個人情報をマスキングし、マスキング後のテキストを生成
4. マスキングした個人情報を抽出し、リストとして保持
5. マスキング後の問い合わせ文と、マスキングした個人情報をカンマ区切りで出力

## 4. 入出力仕様

### 入力
- 顧客からの問い合わせ文テキスト（CSV等の表形式で複数件）

### 出力
- 新規CSVファイルとして出力
- 出力カラム：
  1. 入力データの全カラム
  2. マスキング後の問い合わせ文
  3. マスキングした個人情報（カンマ区切り文字列）
  4. 個人情報検出カウント情報（各種類ごとの検出数）

## 5. 使用技術
- プログラミング言語: Python
- 正規表現: re モジュール
- 自然言語処理: spaCy (日本語モデル: ja_core_news_md)
- データ処理: pandas, numpy
- その他: regex, tqdm

## 6. 環境構築手順

### 6.1 プロジェクト構造
```
PersonalDataMasking/
├── main.py                 # メインエントリーポイント
├── requirements.txt        # 必要なパッケージの一覧
├── config.ini              # 設定ファイル
│
├── data/                   # データディレクトリ
│   ├── input/              # 入力データファイル
│   └── output/             # 出力（マスキング済み）データファイル
│
├── docs/                   # ドキュメント
│   └── 01_NLPによるマスキング.md  # プロジェクト説明書
│
├── logs/                   # ログファイル
│   └── masking.log         # マスキング処理ログ
│
├── scripts/                # 実行スクリプト
│   ├── __init__.py
│   ├── process_data.py     # データ処理実行スクリプト
│   └── test_improvements.py # 改善点テストスクリプト
│
├── src/                    # ソースコード
│   ├── __init__.py
│   ├── config_utils.py     # 設定ファイル読み込み
│   ├── counter.py          # マスキングカウンター
│   ├── masking.py          # マスキング処理コア
│   ├── nlp_utils.py        # NLP関連ユーティリティ
│   └── patterns.py         # マスキングパターン定義
│
├── tests/                  # テストコード・データ
│   ├── __init__.py
│   ├── test_masking.py     # マスキング機能のテスト
│   └── test_data.csv       # テスト用データ
│
└── tools/                  # ユーティリティツール
    ├── __init__.py
    ├── analyze_masking.py  # マスキング結果詳細分析
    ├── analyze_results.py  # 結果集計分析
    └── generate_test_data.py  # テストデータ生成
```

### 6.2 環境セットアップ
1. Python環境の準備（Python 3.8以上を推奨）
2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化（macOS/Linux）
source .venv/bin/activate

# 仮想環境の有効化（Windows）
# .venv\Scripts\activate
```

3. 必要なライブラリのインストール

```bash
# 必要なライブラリのインストール
pip install -r requirements.txt

# spaCyの日本語モデルをインストール
python -m spacy download ja_core_news_md
```

## 7. 使用方法

### 7.1 基本的な使用方法
```bash
python main.py -i [入力CSVファイルパス] -o [出力CSVファイルパス] -c [問い合わせ文のカラム名]
```

### 7.2 オプション
- `-i, --input`: 入力CSVファイルパス（必須）
- `-o, --output`: 出力CSVファイルパス（省略時は自動生成）
- `-c, --column`: 問い合わせ文のカラム名（必須）
- `--no-nlp`: NLP処理を使用しない（正規表現のみでマスキング）

### 7.3 使用例
```bash
# 基本的な使用方法
python main.py -i data/input/customer_inquiries.csv -o data/output/masked_inquiries.csv -c inquiry_text

# NLPなしで実行（処理速度優先）
python main.py -i data/input/customer_inquiries.csv -o data/output/masked_inquiries.csv -c inquiry_text --no-nlp
```

## 8. 今後の展望

1. **精度向上**
   - 日本語固有表現認識の改善（より大きなspaCyモデルの使用検討）

2. **機能拡張**
   - マスキング対象の拡充（クレジットカード番号、マイナンバーなどへの対応）
   - マスキングレベルの設定機能（必要に応じて部分マスキングなど）

3. **パフォーマンス最適化**
   - 大規模データ処理時のメモリ効率化
   - マルチプロセス処理による高速化
