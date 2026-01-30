import pandas as pd
import numpy as np
import sys
sys.path.append(".")

from datetime import datetime, timedelta
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed
from dotenv import dotenv_values

from generated.momentum_score import main

# Load keys
config = dotenv_values(".env")
client = StockHistoricalDataClient(
    config["ALPACA_API_KEY"],
    config["ALPACA_SECRET_KEY"]
)

# Fetch 30 days of data (exclude today)
tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
request = StockBarsRequest(
    symbol_or_symbols=tickers,
    timeframe=TimeFrame.Day,
    start=datetime.now() - timedelta(days=30),
    end=datetime.now() - timedelta(days=1),
    feed=DataFeed.IEX
)
bars = client.get_stock_bars(request).df

# Build market data
market_data = []
for ticker in tickers:
    ticker_data = bars.xs(ticker, level='symbol')
    market_data.append({
        'ticker': ticker,
        'price_20d_ago': ticker_data['close'].iloc[0],
        'price_today': ticker_data['close'].iloc[-1],
        'volume_avg_10d': ticker_data['volume'].tail(10).mean(),
        'volume_today': ticker_data['volume'].iloc[-1]
    })

df = pd.DataFrame(market_data)
print("=== Real Market Data (Alpaca) ===")
print(df)
print()

# Score each asset
results = []
for _, row in df.iterrows():
    result = main(row.to_dict())
    result['ticker'] = row['ticker']
    results.append(result)

results_df = pd.DataFrame(results)
results_df['rank'] = np.argsort(np.argsort(-results_df['score'])) + 1

print("=== Strategy Results ===")
print(results_df.sort_values('score', ascending=False))