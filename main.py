import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED - MULTI ASSET SCANNER")

os.makedirs("output", exist_ok=True)

# -------------------------
# WATCHLIST (EDIT THIS)
# -------------------------
tickers = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "META"]

results = []

# -------------------------
# LOOP THROUGH ASSETS
# -------------------------
for ticker in tickers:
    try:
        price, series = get_data(ticker)

        print(f"Processing {ticker} | Data points: {len(series)}")

        # -------------------------
        # VOLATILITY
        # -------------------------
        returns = np.diff(series) / np.array(series[:-1])
        volatility = np.std(returns) * np.sqrt(252)

        # -------------------------
        # TREND
        # -------------------------
        trend = (series[-1] - series[0]) / series[0]

        # -------------------------
        # DOUBLE DIAGONAL SIGNAL
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
            "Price": price,
            "Trend": trend,
            "Volatility": volatility,
            "Expected_Move": expected_move,
            "Support": support,
            "Resistance": resistance,
            "Signal": signal,
            "Score": score
        })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# -------------------------
# CREATE DATAFRAME
# -------------------------
df = pd.DataFrame(results)

# -------------------------
# SORT BEST SETUPS FIRST
# -------------------------
df = df.sort_values(by="Score", ascending=False)

# -------------------------
# SAVE OUTPUT
# -------------------------
df.to_csv("output/results.csv", index=False)

print("DONE - MULTI ASSET SCAN COMPLETE")
print(df)
