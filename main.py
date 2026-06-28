import os
import numpy as np
import pandas as pd
from market import get_price_and_chain

print("REAL OPTIONS DOUBLE DIAGONAL ENGINE STARTED")

os.makedirs("output", exist_ok=True)

# =========================
# CHANGE YOUR WATCHLIST HERE
# =========================
tickers = ["QQQ", "SPY", "AAPL", "TSLA"]

results = []

for ticker in tickers:
    print(f"\nProcessing {ticker}")

    try:
        price, calls, puts, expiry = get_price_and_chain(ticker)

        print(f"{ticker} PRICE: {price}")
        print(f"EXPIRY USED: {expiry}")

        # -------------------------
        # FIND ATM STRIKES
        # -------------------------
        calls = calls.sort_values("strike")
        puts = puts.sort_values("strike")

        atm_call = calls.iloc[(calls["strike"] - price).abs().argmin()]
        atm_put = puts.iloc[(puts["strike"] - price).abs().argmin()]

        # -------------------------
        # OUTER WINGS (real market strikes)
        # -------------------------
        otm_calls = calls[calls["strike"] > price]
        otm_puts = puts[puts["strike"] < price]

        if len(otm_calls) < 2 or len(otm_puts) < 2:
            print("Not enough strikes")
            continue

        short_call = otm_calls.iloc[0]
        long_call = otm_calls.iloc[2]

        short_put = otm_puts.iloc[-1]
        long_put = otm_puts.iloc[-3]

        # -------------------------
        # REAL PREMIUM COST
        # -------------------------
        debit = (
            long_call["lastPrice"]
            + long_put["lastPrice"]
            - short_call["lastPrice"]
            - short_put["lastPrice"]
        )

        # -------------------------
        # SIGNAL (simple volatility proxy)
        # -------------------------
        expected_move = price * 0.02

        if abs(short_call["strike"] - price) > expected_move:
            signal = "GOOD_SETUP"
            score = 5
        else:
            signal = "OK_SETUP"
            score = 3

        results.append({
            "Ticker": ticker,
            "Price": price,
            "Expiry": expiry,

            "Short_Call_Strike": short_call["strike"],
            "Short_Put_Strike": short_put["strike"],
            "Long_Call_Strike": long_call["strike"],
            "Long_Put_Strike": long_put["strike"],

            "Short_Call_Premium": short_call["lastPrice"],
            "Short_Put_Premium": short_put["lastPrice"],
            "Long_Call_Premium": long_call["lastPrice"],
            "Long_Put_Premium": long_put["lastPrice"],

            "Estimated_Debit": debit,
            "Signal": signal,
            "Score": score
        })

        print(f"{ticker} DONE")

    except Exception as e:
        print(f"{ticker} ERROR: {e}")

# -------------------------
# SAVE OUTPUT
# -------------------------
df = pd.DataFrame(results)

df = df.sort_values("Score", ascending=False)

df.to_csv("output/results.csv", index=False)

print("\nDONE")
print(df)
