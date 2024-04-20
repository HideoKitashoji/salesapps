import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 会社とティッカーシンボルの辞書
company_dict = {
    '富士通': '6702.T',
    'トヨタ': '7203.T',
    'ソニー': '6758.T',
    '任天堂': '7974.T',
    # 他の会社とそのティッカーシンボルを追加
}

# Streamlitのサイドバーで複数の会社を選択できるチェックボックスリストを表示
# デフォルトで"富士通"が選択されている状態にする
selected_companies = st.sidebar.multiselect("会社を選択してください", list(company_dict.keys()), default=["富士通"])

# 選択された会社のデータを保持するリスト
data_list = []

# 選択された会社ごとに財務データを取得
for company in selected_companies:
    # 選択された会社のティッカーシンボルを取得
    ticker_symbol = company_dict[company]
    
    # 選択された会社のティッカーシンボルを使って情報を取得
    ticker_info = yf.Ticker(ticker_symbol)
    
    # 最新の損益計算書、貸借対照表、キャッシュフロー計算書のデータを取得
    df_pl = ticker_info.financials.T.head(1) / 100000000    # 損益計算書
    df_bs = ticker_info.balance_sheet.T.head(1) / 100000000 # 貸借対照表
    df_cf = ticker_info.cashflow.T.head(1) / 100000000      # キャッシュフロー計算書
    
    # 必要なデータを選択
    df1 = df_pl.loc[:, ['Total Revenue', 'Net Income']]
    df2 = df_bs.loc[:, ['Total Assets', 'Stockholders Equity']]
    df3 = df_cf.loc[:, ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow']]
    df_combined = pd.concat([df1, df2, df3], axis=1)
    
    # カラム名を日本語に変更
    japanese_columns = ['総収入', '純利益', '総資産', '株主資本', '営業CF', '投資CF', '財務CF']
    df_combined.columns = japanese_columns
    
    # 純利益と株主資本を取得
    純利益 = df_combined['純利益']
    株主資本 = df_combined['株主資本']
    
    # ROEを計算
    roe = 純利益 / 株主資本
    
    # ROEの列を小数点以下第3位まで丸める
    roe_rounded = roe.round(3)
    
    # ROEの列をデータフレームに追加
    df_combined['ROE'] = roe_rounded
    
    # 会社名のみを文字列に変換
    df_combined['会社名'] = company
    
    # 整数に変換する列を選択
    int_columns = ['総収入', '純利益', '総資産', '株主資本', '営業CF', '投資CF', '財務CF']
    
    # 整数に変換
    df_combined[int_columns] = df_combined[int_columns].astype(int)
    
    # データをリストに追加
    data_list.append(df_combined)

# リストに追加されたデータを結合して1つのデータフレームに変換
df_all_companies = pd.concat(data_list)


# 会社名を先頭に持ってくる
columns_order = ['会社名', '総収入', '純利益', '総資産', '株主資本', '営業CF', '投資CF', '財務CF', 'ROE']

# カラムの順序を変更
df_all_companies = df_all_companies.reindex(columns=columns_order)

# Streamlitで選択された会社の最新年度財務データを表示
st.write(f"最新年度財務データ:")

st.dataframe(df_all_companies, hide_index=True)
