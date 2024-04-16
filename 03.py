import streamlit as st
import yfinance as yf
import pandas as pd

# 会社とティッカーシンボルの辞書
company_dict = {
    '富士通': '6702.T',
    'トヨタ': '7203.T',
    'ソニー': '6758.T',
    '任天堂': '7974.T',
    # 他の会社とそのティッカーシンボルを追加
}

# Streamlitのサイドバーで会社選択のためのドロップダウンメニューを表示
selected_company = st.sidebar.selectbox("会社を選択してください", list(company_dict.keys()))

# 選択された会社のティッカーシンボルを取得
ticker_symbol = company_dict[selected_company]

# 選択された会社のティッカーシンボルを使って情報を取得
ticker_info = yf.Ticker(ticker_symbol)

# 損益計算書、貸借対照表、キャッシュフロー計算書のデータを取得
df_pl = ticker_info.financials / 100000000    # 損益計算書
df_bs = ticker_info.balance_sheet / 100000000 # 貸借対照表
df_cf = ticker_info.cashflow / 100000000      # キャッシュフロー計算書

# 必要なデータを選択
df1 = df_pl.loc[['Total Revenue', 'Net Income']].T
df2 = df_bs.loc[['Total Assets', "Stockholders Equity"]].T
df3 = df_cf.loc[['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow']].T
df_combined = pd.concat([df1, df2, df3], axis=1)

# 純利益と株主資本を取得
net_income = df_combined['Net Income']
stockholders_equity = df_combined['Stockholders Equity']

# ROEを計算
roe = net_income / stockholders_equity

# df_combinedにROEの値を新しいカラムとして追加
df_combined['ROE'] = roe

# Streamlitでデータを表示
st.write(f"{selected_company}の過去3年分財務データ:")
st.write(df_combined)
