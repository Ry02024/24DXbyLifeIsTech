import pandas as pd
import yaml
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt

def apply_and_load_label_encoding(df, filepath):
    """
    YAMLファイルからラベルエンコーディング情報を取得し、商品カテゴリに適用する関数。
    
    Parameters:
        df (pd.DataFrame): データフレーム。
        filepath (str): YAMLファイルへのパス。
    
    Returns:
        pd.DataFrame, LabelEncoder: ラベルエンコーディングが適用されたデータフレームとLabelEncoderオブジェクト。
    """
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)

    label_encoder_info = config['label_encoding']
    le = LabelEncoder()
    le.classes_ = np.array(label_encoder_info['商品カテゴリ'])  # ラベルエンコーディングを設定

    df['商品カテゴリ'] = le.transform(df['商品カテゴリ'])  # 商品カテゴリにラベルエンコーディングを適用
    return df, le


def plot_sales_comparison(total_actual_sales, total_predicted_sales):
    """
    予測売上と実売上を棒グラフで比較する関数。
    
    Parameters:
        total_actual_sales (float): 実売上の合計。
        total_predicted_sales (float): 予測売上の合計。
    
    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    categories = ['実売上', '予測売上']
    values = [total_actual_sales, total_predicted_sales]

    plt.bar(categories, values, color=['green', 'blue'])
    plt.title('実売上と予測売上の比較')
    plt.ylabel('売上 (¥)')
    plt.grid(True)
    plt.show()


def plot_category_sales_comparison(df):
    """
    商品カテゴリごとの予測売上と実売上を比較する棒グラフを作成する関数。
    
    Parameters:
        df (pd.DataFrame): データフレーム。
    
    Returns:
        None
    """
    category_sales_actual = df.groupby('商品カテゴリ')['実売上'].sum()
    category_sales_predicted = df.groupby('商品カテゴリ')['売上予測'].sum()

    plt.figure(figsize=(12, 6))
    category_labels = category_sales_actual.index

    plt.bar(category_labels, category_sales_actual, width=0.4, label='実売上', align='center', color='green')
    plt.bar(category_labels, category_sales_predicted, width=0.4, label='予測売上', align='edge', color='blue')

    plt.title('商品カテゴリごとの実売上と予測売上の比較')
    plt.xlabel('商品カテゴリ')
    plt.ylabel('売上 (¥)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def sim(scenario_df, filepath, model, selected_columns):
    """
    シナリオデータを使って一連の処理（ラベルエンコーディング、予測、売上計算、売上比較グラフ）を実行する関数。
    
    Parameters:
        scenario_df (pd.DataFrame): シナリオデータ。
        filepath (str): ラベルエンコーディング情報が含まれるYAMLファイルへのパス。
        model (lgb.Booster): 予測に使用するLightGBMモデル。
        selected_columns (list): 予測に使用する説明変数のカラムリスト。
    
    Returns:
        None
    """
    # --- 1. ラベルエンコーディングの適用と情報の取得 ---
    scenario_df, le = apply_and_load_label_encoding(scenario_df, filepath)
    # --- 2. LightGBMモデルに渡す前にカテゴリカルデータを指定 ---
    scenario_df['商品ID'] = scenario_df['商品ID'].astype('category')  # 商品IDをカテゴリカル型に変換
    categorical_features = ['商品ID', '商品カテゴリ']  # LightGBMのカテゴリカル変数として指定
    
    # --- 3. 予測の実行 ---
    y_pred = model.predict(scenario_df[selected_columns], num_iteration=model.best_iteration)
    # --- 4. 売上の計算 ---
    scenario_df['売上予測'] = y_pred * scenario_df['商品単価']
    scenario_df['実売上'] = scenario_df['売上']
    # --- 5. 商品カテゴリをデコード ---
    scenario_df['商品カテゴリ'] = le.inverse_transform(scenario_df['商品カテゴリ'])
    
    # --- 6. 総売上の計算 ---
    total_predicted_sales = scenario_df['売上予測'].sum()
    total_actual_sales = scenario_df['実売上'].sum()
    # --- 7. 売上の変化を表示 ---
    print(f"予測売上の合計: {total_predicted_sales:.2f}円")
    print(f"実売上の合計: {total_actual_sales:.2f}円")
    sales_change = total_predicted_sales - total_actual_sales
    print(f"売上の変化: {sales_change:.2f}円")
    # --- 8. 売上比較のグラフ表示 ---
    plot_sales_comparison(total_actual_sales, total_predicted_sales)
    
    # --- 9. 商品カテゴリごとの売上比較のグラフ表示 ---
    plot_category_sales_comparison(scenario_df)
