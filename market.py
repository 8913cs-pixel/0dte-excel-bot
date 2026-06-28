import yfinance as yf
import pandas as pd

def get_data(ticker, period="5d", interval="5m"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)

    if df is None or df.empty:
        raise ValueError(f"No data for {ticker}")

    close = df["Close"]

    # FORCE SAFE CONVERSION (fixes your error)
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    series = close.dropna().astype(float).values.tolist()
    price = float(series[-1])

    return price, series
