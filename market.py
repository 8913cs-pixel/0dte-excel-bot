import yfinance as yf

def get_data(ticker):
    data = yf.download(ticker, period="5d", interval="1h", progress=False)

    if data is None or data.empty:
        raise Exception("No data from yfinance")

    close = data["Close"].dropna()

    if len(close) < 2:
        raise Exception("Not enough data")

    return close.iloc[-1], close.tolist()
