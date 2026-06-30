import pandas as pd
from market import get_price_and_chains


TICKER = "QQQ"
OUTPUT_FILE = "output/results.csv"


def build_double_diagonal(price,
                          front_calls, front_puts, front_expiry,
                          back_calls, back_puts, back_expiry):

    front_calls = front_calls.sort_values("strike")
    front_puts = front_puts.sort_values("strike")
    back_calls = back_calls.sort_values("strike")
    back_puts = back_puts.sort_values("strike")

    # OTM filtering
    front_otm_calls = front_calls[front_calls["strike"] > price]
    front_otm_puts = front_puts[front_puts["strike"] < price]

    back_otm_calls = back_calls[back_calls["strike"] > price]
    back_otm_puts = back_puts[back_puts["strike"] < price]

    if len(front_otm_calls) < 1 or len(front_otm_puts) < 1:
        return None
    if len(back_otm_calls) < 3 or len(back_otm_puts) < 3:
        return None

    # Front expiry = shorts
    short_call = front_otm_calls.iloc[0]
    short_put = front_otm_puts.iloc[-1]

    # Back expiry = longs
    long_call = back_otm_calls.iloc[2]
    long_put = back_otm_puts.iloc[-3]

    debit = (
        long_call["lastPrice"]
        + long_put["lastPrice"]
        - short_call["lastPrice"]
        - short_put["lastPrice"]
    )

    return {
        "Ticker": TICKER,
        "Underlying": price,

        "Short_Call_Strike": short_call["strike"],
        "Short_Put_Strike": short_put["strike"],
        "Long_Call_Strike": long_call["strike"],
        "Long_Put_Strike": long_put["strike"],

        "Short_Expiry": front_expiry,
        "Long_Expiry": back_expiry,

        "Net_Debit": round(debit, 2),
    }


def run():
    (
        price,
        front_calls,
        front_puts,
        front_expiry,
        back_calls,
        back_puts,
        back_expiry,
    ) = get_price_and_chains(TICKER)

    trade = build_double_diagonal(
        price,
        front_calls, front_puts, front_expiry,
        back_calls, back_puts, back_expiry,
    )

    if trade is None:
        print("No valid setup found")
        return

    df = pd.DataFrame([trade])
    df.to_csv(OUTPUT_FILE, index=False)

    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    run()
