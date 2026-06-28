import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED - DEBUG MODE")

os.makedirs("output", exist_ok=True)

tickers = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "META"]

results = []

def round_strike(x):
    return round(x / 5) * 5


for ticker in tickers:
    print(f"\n--- Processing {ticker} ---")

    try:
        price, series = get_data(ticker)

        print(f"{ticker} price: {price}")
        print(f"{ticker} data points: {len(series)}")

        # 🔥 IMPORTANT CHECK
        if series is None or len(series) < 20:
            print(f"SKIP {ticker} (not enough data)")
            continue

        series = np.array(series, dtype=float)

        returns = np.diff(series) / series[:-1]
        volatility = np.std(returns) * np.sqrt(252)

        trend = (series[-1] - series[0]) / series[0]

        expected_move = price * volatility * 0.1

        upper = price + expected_move
        lower = price - expected_move

        short_call = round_strike(upper)
        short_put = round_strike(lower)

        long_call = round_strike(upper + expected_move * 0.5)
        long_put = round_strike(lower - expected_move * 0.5)

        estimated_debit = 2.5 * (1 + volatility * 5)

        signal = "DOUBLE_DIAGONAL" if abs(trend) < 0.02 else "AVOID"
        score = 5 if signal == "DOUBLE_DIAGONAL" else 0

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

        print(f"{ticker} OK → added to results")

    except Exception as e:
        print(f"ERROR {ticker}: {e}")


# -------------------------
# SAVE FILE
# -------------------------
df = pd.DataFrame(results)

print("\nFINAL ROW COUNT:", len(df))

file_path = "output/results.csv"
df.to_csv(file_path, index=False)

print(f"FILE SAVED: {file_path}")
print(df)
