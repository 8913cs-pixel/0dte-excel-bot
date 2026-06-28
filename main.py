import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED - DOUBLE DIAGONAL SCANNER")

os.makedirs("output", exist_ok=True)

# =========================
# WATCHLIST (CHANGE HERE)
# =========================
tickers = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "META"]

results = []

# =========================
# HELPERS
# =========================
def round_strike(x):
    return round(x / 5) * 5


# =========================
# MAIN LOOP
# =========================
for ticker in tickers:
    try:
        price, series = get_data(ticker)

        print(f"\nProcessing {ticker} | Points: {len(series)}")

        if len(series) < 10:
            print(f"Skipping {ticker} (not enough data)")
            continue

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
        # ESTIMATED ENTRY COST (SIMPLIFIED MODEL)
        # -------------------------
        base_cost = 2.5
        estimated_debit = base_cost * (1 + volatility * 5)

        # -------------------------
        # SIGNAL LOGIC
        # -------------------------
        if abs(trend) < 0.01 and volatility > 0.15:
            signal = "STRONG_DOUBLE_DIAGONAL"
            score = 5
        elif abs(trend) < 0.02:
            signal = "WEAK_DOUBLE_DIAGONAL"
            score = 3
        else:
            signal = "AVOID_TREND"
            score = 0

        # -------------------------
        # STORE RESULT
        # -------------------------
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

    except Exception as e:
        print(f"Error {ticker}: {e}")


# =========================
# SAVE OUTPUT
# =========================
df = pd.DataFrame(results)

if df.empty:
    print("NO DATA GENERATED")
    df.to_csv("output/results.csv", index=False)
else:
    df = df.sort_values(by="Score", ascending=False)
    df.to_csv("output/results.csv", index=False)

    print("\nTOP SETUPS:")
    print(df.head())

print("\nDONE")
