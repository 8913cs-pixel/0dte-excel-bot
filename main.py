import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED - MULTI ASSET SCANNER")

os.makedirs("output", exist_ok=True)

# -------------------------
# WATCHLIST
# -------------------------
tickers = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "META"]

results = []

# -------------------------
# SCAN ALL TICKERS
# -------------------------
for ticker in tickers:
    try:
        price, series = get_data(ticker)

        print(f"Processing {ticker} | Data points: {len(series)}")

        # Safety check
        if len(series) < 2:
            print(f"Not enough data for {ticker}")
            continue

        series = np.array(series, dtype=float)

        # -------------------------
        # RETURNS + VOLATILITY
        # -------------------------
        returns = np.diff(series) / series[:-1]
        volatility = np.std(returns) * np.sqrt(252)

        # -------------------------
        # TREND
        # -------------------------
        trend = (series[-1] - series[0]) / series[0]

        # -------------------------
        # DOUBLE DIAGONAL SIGNAL LOGIC
        # -------------------------
        if abs(trend) < 0.01 and volatility > 0.15:
            signal = "GOOD_DOUBLE_DIAGONAL"
            score = 3
        elif abs(trend) < 0.02:
            signal = "OK_SETUP"
            score = 2
        else:
            signal = "AVOID_TRENDING"
            score = 0

        # -------------------------
        # EXPECTED MOVE
        # -------------------------
        expected_move = price * volatility * 0.1
        support = price - expected_move
        resistance = price + expected_move

        results.append({
            "Ticker": ticker,
            "Price": float(price),
            "Trend": float(trend),
            "Volatility": float(volatility),
            "Expected_Move": float(expected_move),
            "Support": float(support),
            "Resistance": float(resistance),
            "Signal": signal,
            "Score": int(score)
        })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# -------------------------
# CREATE DATAFRAME SAFELY
# -------------------------
df = pd.DataFrame(results)

# -------------------------
# SAVE EVEN IF EMPTY (NO CRASH)
# -------------------------
if df.empty:
    print("NO VALID DATA FOUND - CHECK MARKET DATA")
    df.to_csv("output/results.csv", index=False)
else:
    df = df.sort_values(by="Score", ascending=False)
    df.to_csv("output/results.csv", index=False)

    print("\nTOP SETUPS:")
    print(df.head())

print("DONE - BOT FINISHED")
