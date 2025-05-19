"""
設定ファイル管理ユーティリティ
"""
import configparser
from pathlib import Path


def load_config(config_file='config.ini'):
    """
    設定ファイルを読み込む

    Args:
        config_file (str): 設定ファイルパス

    Returns:
        configparser.ConfigParser: 設定オブジェクト
    """
    config = configparser.ConfigParser()
    config_path = Path(config_file)

    # デフォルト設定
    config['masking'] = {
        'name_placeholder': '[氏名]',
        'phone_placeholder': '[電話番号]',
        'email_placeholder': '[メールアドレス]',
        'address_placeholder': '[住所]',
        'date_placeholder': '[日付]',
        'birthdate_placeholder': '[生年月日]',
        'company_placeholder': '[企業情報]'
    }

    config['output'] = {
        'timestamp_format': '%Y%m%d%H%M%S',
        'encoding': 'utf-8'
    }

    config['logging'] = {
        'level': 'INFO',
        'log_file': 'logs/masking.log'
    }

    config['nlp'] = {
        'japanese_model': 'ja_core_news_md'
    }

    # 設定ファイルが存在すれば読み込む
    if config_path.exists():
        config.read(config_path)

    return config


if __name__ == "__main__":
    # 設定ファイルのテスト読み込み
    config = load_config()

    # 読み込んだ設定を表示
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config[section].items():
            print(f"{key} = {value}")
        print()
