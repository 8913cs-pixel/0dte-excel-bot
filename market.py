import yfinance as yf

def get_data(ticker, period="5d", interval="5m"):
    df = yf.download(ticker, period=period, interval=interval)

    if df.empty:
        raise ValueError("No data returned from Yahoo Finance")

    series = df["Close"].dropna().tolist()
    price = series[-1]

    return price, series
