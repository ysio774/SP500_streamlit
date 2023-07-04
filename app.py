import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

# データ取得期間を設定します。今回は過去20年間のデータを取得します。
end_date = datetime.now()
start_date = end_date - timedelta(days=26*365)  # 26年前

# Yahoo FinanceからS&P 500, Nikkkei225とUSD/JPYのデータを取得します。
sp500 = yf.download('^GSPC', start=start_date, end=end_date)
usd_jpy = yf.download('JPY=X', start=start_date, end=end_date)


# S&P 500の価格を円に変換します。
sp500_in_jpy = sp500['Close'] * usd_jpy['Close']
sp500_in_jpy.dropna(inplace=True)  # データの欠損値を削除します。

# データとタイトルをペアにしたリストを作成
data_and_titles = [
    (sp500['Close'], 'S&P 500 (USD)'),
    (usd_jpy['Close'], 'USD/JPY Rate'),
    (sp500_in_jpy, 'S&P 500 (JPY)')
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
    fig.show()