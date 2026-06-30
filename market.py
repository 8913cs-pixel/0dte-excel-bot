import yfinance as yf


def get_price_and_chains(ticker: str):
    t = yf.Ticker(ticker)

    hist = t.history(period="1d", interval="1m")
    if hist is None or hist.empty:
        raise ValueError("No price data found")

    price = float(hist["Close"].iloc[-1])

    expirations = t.options
    if len(expirations) < 2:
        raise ValueError("Need at least 2 expirations")

    # Front + Back expiry (Double Diagonal structure)
    front_expiry = expirations[0]
    back_expiry = expirations[min(2, len(expirations) - 1)]

    front_chain = t.option_chain(front_expiry)
    back_chain = t.option_chain(back_expiry)

    return (
        price,
        front_chain.calls,
        front_chain.puts,
        front_expiry,
        back_chain.calls,
        back_chain.puts,
        back_expiry,
    )
