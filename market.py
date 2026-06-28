import yfinance as yf

def get_data(ticker):
    df = yf.download(
        ticker,
        period="1d",
        interval="1m",
        progress=False,
        threads=False
    )

    if df is None or df.empty:
        raise ValueError(f"No data for {ticker}")

    # 🔥 REAL-TIME LAST PRICE (THIS FIXES YOUR 380 PROBLEM)
    price = float(df["Close"].dropna().iloc[-1])

    # full intraday series
    series = df["Close"].dropna().astype(float).tolist()

    return price, series
