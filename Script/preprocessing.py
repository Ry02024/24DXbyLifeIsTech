# 年齢の正規化関数に NaN の処理を追加
def normalize_age(age):
    if pd.isna(age):
        return '不明'
    elif '10代' in age:
        return '10代'
    elif '20代' in age:
        return '20代'
    elif '30代' in age:
        return '30代'
    elif '40代' in age:
        return '40代'
    elif '50代' in age:
        return '50代'
    elif '60代' in age:
        return '60代'
    elif '70代' in age or '70代以上' in age:
        return '70代以上'
    else:
        return 'その他'

# 取引日時から時間帯を抽出する関数
def extract_time_band(df, datetime_column, new_column='時間帯'):
    """
    データフレームの指定された日時列から時間帯を抽出し、新しい列に追加する関数。

    Parameters:
    df (pd.DataFrame): データフレーム
    datetime_column (str): 日時データが含まれる列名
    new_column (str): 抽出された時間帯を保存する新しい列名（デフォルトは '時間帯'）

    Returns:
    pd.DataFrame: 元のデータフレームに時間帯が追加されたもの
    """
    # 日時列を datetime 型に変換
    df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')

    # 時間帯を抽出して新しい列に保存
    df[new_column] = df[datetime_column].dt.floor('H')

    return df
