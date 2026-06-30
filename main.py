import os
import pandas as pd
from market import get_price_and_chain

TICKER = "QQQ"
OUTPUT_FILE = "output/results.csv"


def run():

    price, calls, puts, expiry = get_price_and_chain(TICKER)

    calls = calls.sort_values("strike")
    puts = puts.sort_values("strike")

    otm_calls = calls[calls["strike"] > price]
    otm_puts = puts[puts["strike"] < price]

    if len(otm_calls) < 3 or len(otm_puts) < 3:
        print("Not enough strikes")
        return

    short_call = otm_calls.iloc[0]
    long_call = otm_calls.iloc[2]

    short_put = otm_puts.iloc[-1]
    long_put = otm_puts.iloc[-3]

    debit = (
        long_call["lastPrice"]
        + long_put["lastPrice"]
        - short_call["lastPrice"]
        - short_put["lastPrice"]
    )

    # ONLY FIX (required for GitHub Actions)
    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame([{
        "Ticker": TICKER,
        "Price": price,
        "Short_Call_Strike": short_call["strike"],
        "Long_Call_Strike": long_call["strike"],
        "Short_Put_Strike": short_put["strike"],
        "Long_Put_Strike": long_put["strike"],
        "Expiry": expiry,
        "Net_Debit": debit
    }])

    df.to_csv(OUTPUT_FILE, index=False)

    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    run()
