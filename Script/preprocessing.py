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
