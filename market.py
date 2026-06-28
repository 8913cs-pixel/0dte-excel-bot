import yfinance as yf

def get_data(ticker, period="5d", interval="5m"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)

    if df is None or df.empty:
        raise ValueError(f"No data for {ticker}")

    series = df["Close"].dropna().astype(float).tolist()
    price = series[-1]

    return price, series
