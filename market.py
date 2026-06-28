import yfinance as yf
import numpy as np

def get_data(ticker):
    try:
        df = yf.download(
            ticker,
            period="1mo",
            interval="15m",
            progress=False,
            threads=False
        )

        if df is None or df.empty:
            raise Exception("Yahoo returned empty data")

        series = df["Close"].dropna().astype(float).tolist()
        price = series[-1]

        return price, series

    except Exception as e:
        print(f"[FALLBACK ACTIVE] {ticker} → {e}")

        # -------------------------
        # SAFE FAKE DATA (ENSURES OUTPUT)
        # -------------------------
        base_prices = {
            "SPY": 450,
            "QQQ": 380,
            "AAPL": 190,
            "TSLA": 250,
            "NVDA": 600,
            "META": 350
        }

        base = base_prices.get(ticker, 100)

        series = list(base + np.random.randn(60).cumsum())
        price = series[-1]

        return price, series
