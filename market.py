import yfinance as yf
import numpy as np

def get_data(ticker):
    try:
        df = yf.download(
            ticker,
            period="5d",
            interval="5m",
            progress=False,
            threads=False
        )

        # If data exists → use it
        if df is not None and not df.empty:
            close = df["Close"].dropna().astype(float)

            if len(close) > 0:
                price = float(close.iloc[-1])
                series = close.tolist()
                return price, series

        # If empty → force fallback
        raise Exception("Empty or invalid data")

    except Exception as e:
        print(f"[FALLBACK USED] {ticker} → {e}")

        # -------------------------
        # SAFE SYNTHETIC DATA (NEVER FAILS)
        # -------------------------
        base_prices = {
            "SPY": 450,
            "QQQ": 710,
            "AAPL": 190,
            "TSLA": 250,
            "NVDA": 600,
            "META": 350
        }

        base = base_prices.get(ticker, 100)

        series = list(base + np.random.randn(80).cumsum())
        price = series[-1]

        return price, series
