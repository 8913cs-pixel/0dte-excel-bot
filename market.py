import yfinance as yf

def get_price_and_chain(ticker):
    t = yf.Ticker(ticker)

    # -------------------------
    # REAL-TIME UNDERLYING PRICE
    # -------------------------
    hist = t.history(period="1d", interval="1m")

    if hist is None or hist.empty:
        raise ValueError("No price data")

    price = float(hist["Close"].iloc[-1])

    # -------------------------
    # OPTION CHAIN (nearest expiry)
    # -------------------------
    expirations = t.options

    if not expirations:
        raise ValueError("No options available")

    nearest_expiry = expirations[0]

    chain = t.option_chain(nearest_expiry)

    calls = chain.calls
    puts = chain.puts

    return price, calls, puts, nearest_expiry
