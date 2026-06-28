import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED - STABLE DOUBLE DIAGONAL SCANNER")

os.makedirs("output", exist_ok=True)

# =========================
# 🔥 EDIT YOUR STOCK LIST HERE
# =========================
tickers = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "META"]

results = []

def round_strike(x):
    return round(x / 5) * 5


for ticker in tickers:
    print(f"\nProcessing {ticker}")

    try:
        price, series = get_data(ticker)

        print(f"{ticker} price: {price} | points: {len(series)}")

        series = np.array(series, dtype=float)

        # -------------------------
        # VOLATILITY
        # -------------------------
        returns = np.diff(series) / series[:-1]
        volatility = np.std(returns) * np.sqrt(252)

        # -------------------------
        # TREND
        # -------------------------
        trend = (series[-1] - series[0]) / series[0]

        # -------------------------
        # EXPECTED MOVE
        # -------------------------
        expected_move = price * volatility * 0.1

        upper = price + expected_move
        lower = price - expected_move

        # -------------------------
        # STRIKES (DOUBLE DIAGONAL)
        # -------------------------
        short_call = round_strike(upper)
        short_put = round_strike(lower)

        long_call = round_strike(upper + expected_move * 0.5)
        long_put = round_strike(lower - expected_move * 0.5)

        # -------------------------
        # COST ESTIMATE
        # -------------------------
        estimated_debit = 2.5 * (1 + volatility * 5)

        # -------------------------
        # SIGNAL LOGIC
        # -------------------------
        if abs(trend) < 0.015 and volatility > 0.12:
            signal = "BEST_DOUBLE_DIAGONAL"
            score = 5
        elif abs(trend) < 0.025:
            signal = "OK_SETUP"
            score = 3
        else:
            signal = "AVOID_TREND"
            score = 0

        results.append({
            "Ticker": ticker,
            "Price": float(price),
            "Trend": float(trend),
            "Volatility": float(volatility),

            "Expected_Move": float(expected_move),

            "Short_Put": short_put,
            "Short_Call": short_call,
            "Long_Put": long_put,
            "Long_Call": long_call,

            "Estimated_Debit": float(estimated_debit),

            "Signal": signal,
            "Score": score
        })

        print(f"{ticker} → ADDED")

    except Exception as e:
        print(f"{ticker} ERROR → {e}")


# =========================
# SAVE (NEVER EMPTY)
# =========================
df = pd.DataFrame(results)

print("\nTOTAL ROWS GENERATED:", len(df))

df.to_csv("output/results.csv", index=False)

print("FILE SAVED → output/results.csv")
print(df)
