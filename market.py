import yfinance as yf

def get_data(ticker):
    # =========================
    # 🔥 CHANGE DATA QUALITY HERE
    # =========================
    df = yf.download(
        ticker,
        period="1mo",
        interval="15m",
        progress=False
    )

    if df is None or df.empty:
        raise ValueError(f"No data for {ticker}")

    series = df["Close"].dropna().astype(float).tolist()
    price = series[-1]

    return price, series
