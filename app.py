import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

end = datetime.today()
start = end - timedelta(days=26*365)

hist_sp500 = yf.Ticker('^GSPC').history(start=start, end=end)
hist_n225 = yf.Ticker('^N225').history(start=start, end=end)
hist_usd_jpy = yf.Ticker('JPY=X').history(start=start, end=end)

hist_sp500 = hist_sp500['Close']
hist_sp500.index = hist_sp500.index.strftime('%Y-%m-%d')
hist_n225 = hist_n225['Close']
hist_n225.index = hist_n225.index.strftime('%Y-%m-%d')
hist_usd_jpy = hist_usd_jpy['Close']
hist_usd_jpy.index = hist_usd_jpy.index.strftime('%Y-%m-%d')

hist_sp500_in_jpy = hist_sp500 * hist_usd_jpy
hist_sp500_in_jpy.dropna(inplace=True) 
hist_n225_in_usd = hist_n225 / hist_usd_jpy
hist_n225_in_usd.dropna(inplace=True) 

# データとタイトルをペアにしたリストを作成
data_and_titles = [
    (hist_sp500, 'S&P 500 (USD)'),
    (hist_n225_in_usd, 'Nikkei 225 (USD)'),
    (hist_usd_jpy, 'USD/JPY Rate'),
    (hist_sp500_in_jpy, 'S&P 500 (JPY)'),
    (hist_n225, 'Nikkei 225 (JPY)')
]

# 各データに対してグラフを作成
for data, title in data_and_titles:
    fig = go.Figure()

    # データのラインを追加
    fig.add_trace(go.Scatter(x=data.index, y=data, name=title))

    # レイアウトを設定
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value',
        xaxis_rangeslider_visible=True  # スライダーを表示
    )

    # グラフを表示
    st.plotly_chart(fig) 
