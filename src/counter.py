"""
マスキングした情報のカウント機能
"""
from collections import Counter

def count_masked_info(masked_items):
    """
    マスキングされた個人情報の種類ごとのカウントを行う

    Args:
        masked_items (list): マスキングされた項目のリスト

    Returns:
        dict: タイプごとのカウント情報
    """
    if not masked_items:
        return {
            'name': 0,
            'phone': 0,
            'date': 0,
            'email': 0,
            'address': 0,
            'company': 0,
            'total': 0
        }

    # カウンターを作成
    counter = Counter()

    # 各マスキングアイテムをカウント
    for item in masked_items:
        item_type = item.split(':')[0] if ':' in item else 'unknown'
        counter[item_type] += 1

    # 結果を辞書として整形
    result = {
        'name': counter.get('name', 0),
        'phone': counter.get('phone', 0),
        'date': counter.get('date', 0),
        'email': counter.get('email', 0),
        'address': counter.get('address', 0),
        'company': counter.get('company', 0),
    }

    # 合計を追加
    result['total'] = sum(result.values())

    return result

def format_count_result(count_dict):
    """
    カウント結果を文字列フォーマットに変換する

    Args:
        count_dict (dict): タイプごとのカウント情報

    Returns:
        str: フォーマットされたカウント情報
    """
    formatted = []

    for key, value in count_dict.items():
        if key != 'total':
            formatted.append(f"{key}:{value}")

    formatted.append(f"total:{count_dict['total']}")

    return ','.join(formatted)