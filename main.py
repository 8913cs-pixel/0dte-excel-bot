import os
import numpy as np
import pandas as pd
from market import get_data

print("BOT STARTED")

os.makedirs("output", exist_ok=True)

ticker = "SPY"

price, series = get_data(ticker)

print("DATA LENGTH:", len(series))

# -------------------------
# VOLATILITY CALCULATION
# -------------------------
returns = np.diff(series) / np.array(series[:-1])
volatility = np.std(returns) * np.sqrt(252)

# -------------------------
# TREND CALCULATION
# -------------------------
trend = (series[-1] - series[0]) / series[0]

# -------------------------
# DOUBLE DIAGONAL LOGIC
# -------------------------
if abs(trend) < 0.01 and volatility > 0.15:
    signal = "DOUBLE_DIAGONAL_SETUP"
elif abs(trend) > 0.02:
    signal = "TRENDING_MARKET_AVOID"
else:
    signal = "NEUTRAL_WAIT"

# -------------------------
# EXPECTED MOVE (simple model)
# -------------------------
expected_move = price * volatility * 0.1

support = price - expected_move
resistance = price + expected_move

# -------------------------
# SAVE OUTPUT
# -------------------------
df = pd.DataFrame([{
    "Ticker": ticker,
    "Price": price,
    "Trend": trend,
    "Volatility": volatility,
    "Expected_Move": expected_move,
    "Support": support,
    "Resistance": resistance,
    "Signal": signal
}])

df.to_csv("output/results.csv", index=False)

print("DONE - CSV CREATED")
print(df)
