# 個人情報マスキングプログラム

![GitHub language](https://img.shields.io/badge/language-Python-blue)
![GitHub license](https://img.shields.io/badge/license-MIT-green)

顧客問い合わせデータから個人情報を自動検出し、マスキング処理を行うPythonプログラムです。

## 概要

企業の顧客サポート部門で扱われる問い合わせデータには、個人情報が含まれることがあります。このプログラムは、そのような個人情報を自動検出し、適切にマスキングすることで、データの匿名化と安全な分析を可能にします。

## 主な機能

- 日本語テキスト内の個人情報を自動検出
- 検出した個人情報を適切なマスキング記号に置換
- 氏名、電話番号、メールアドレス、生年月日、住所、企業情報などに対応
- 一般の日付と生年月日を文脈から区別
- CSVファイル形式の一括処理
- マスキング結果の統計・分析機能

## 使い方

### 基本的な使い方

```
python main.py -i <入力CSVファイル> -o <出力CSVファイル> -c <処理対象カラム名>
```

### オプション

- `-i, --input` : 入力CSVファイルパス (必須)
- `-o, --output` : 出力CSVファイルパス (省略時は自動生成)
- `-c, --column` : 処理対象となるテキストカラム名 (必須)
- `--no-nlp` : NLP処理を使用しない (高速だが精度が低下)

### 使用例

```bash
# 基本的な使用方法
python main.py -i data/input/customer_inquiries.csv -o data/output/masked_inquiries.csv -c inquiry_text

# NLP処理を無効にして高速処理
python main.py -i data/input/customer_inquiries.csv -c inquiry_text --no-nlp
```

## プロジェクト構造

```
PersonalDataMasking/
├── main.py                 # メインエントリーポイント
├── requirements.txt        # 必要なパッケージの一覧
│
├── data/                   # データディレクトリ
│   ├── input/              # 入力データファイル
│   └── output/             # 出力（マスキング済み）データファイル
│
├── docs/                   # 詳細なドキュメント
│   └── readme.md           # 詳細な仕様書
│
├── logs/                   # ログファイル
│
├── scripts/                # 実行スクリプト
│   ├── process_data.py     # データ処理実行スクリプト
│   └── test_improvements.py # 改善点テストスクリプト
│
├── src/                    # ソースコード
│   ├── counter.py          # マスキングカウンター
│   ├── masking.py          # マスキング処理コア
│   ├── nlp_utils.py        # NLP関連ユーティリティ
│   └── patterns.py         # マスキングパターン定義
│
├── tests/                  # テストコード・データ
│   ├── test_masking.py     # マスキング機能のテスト
│   └── test_data.csv       # テストデータ
│
└── tools/                  # ユーティリティツール
    ├── analyze_masking.py  # マスキング結果詳細分析
    ├── analyze_results.py  # 結果集計分析
    └── generate_test_data.py # テストデータ生成
```

## 前提条件

- Python 3.8以上
- 必要なライブラリ: pandas, numpy, spaCy (日本語モデル)

## インストール方法

1. リポジトリをクローン
   ```bash
   git clone https://github.com/yourusername/PersonalDataMasking.git
   cd PersonalDataMasking
   ```

2. 必要なパッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```

3. spaCyの日本語モデルをインストール
   ```bash
   python -m spacy download ja_core_news_md
   ```

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 詳細なドキュメント

詳細な仕様や設計に関するドキュメントは[docs/readme.md](docs/readme.md)を参照してください。
