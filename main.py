import os
import pandas as pd
from market import get_data

print("BOT STARTED")

os.makedirs("output", exist_ok=True)

ticker = "SPY"

price, series = get_data(ticker)

print("DATA LENGTH:", len(series))

trend = abs((series[-1] - series[0]) / series[0])

risk_score = 0
if trend > 0.02:
    risk_score += 3

signal = "TRADE" if risk_score < 3 else "NO TRADE"

df = pd.DataFrame([{
    "Ticker": ticker,
    "Price": price,
    "Trend": trend,
    "Risk": risk_score,
    "Signal": signal
}])

df.to_csv("output/results.csv", index=False)

print("DONE - CSV CREATED")
