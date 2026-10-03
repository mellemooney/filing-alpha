import csv
from pathlib import Path
import matplotlib.pyplot as plot

ticker = input("Ticker: ").strip().upper()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
file_path = PROJECT_ROOT / "data" / "processed" / f"{ticker}_annual_summary.csv"

with open(file_path, "r", newline = "", encoding = "utf-8") as file:
    rows = list(csv.DictReader(file))

years = []
revenue_billions = []
operating_margins = []
net_margins = []

for row in rows:
    years.append(row["end"][:4])
    revenue_billions.append(float(row["revenue"]) / 1000000000)
    operating_margins.append(float(row["operating margin pct"]))
    net_margins.append(float(row["net margin pct"]))

fig, ax = plot.subplots(figsize = (8,5))
margin_fig, margin_ax = plot.subplots(figsize=(8, 5))

ax.bar(years, revenue_billions)
ax.set_title(f"{ticker} Annual Revenue")
ax.set_xlabel("Fiscal year")
ax.set_ylabel("Revenue (USD billions)")

margin_ax.plot(
    years,
    net_margins,
    marker="o",
    label="Net margin"
)

margin_ax.plot(
    years,
    operating_margins,
    marker="o",
    label="Operating margin"
)


margin_ax.set_title(f"{ticker} Annual Profit Margins")
margin_ax.set_xlabel("Fiscal year")
margin_ax.set_ylabel("Margin (%)")
margin_ax.legend()
margin_ax.grid(axis="y", alpha=0.3)


margin_path = PROJECT_ROOT / "data" / "processed" / f"{ticker}_margins.png"
revenue_path = PROJECT_ROOT / "data" / "processed" / f"{ticker}_revenue.png"
fig.savefig(revenue_path, dpi=150)
margin_fig.savefig(margin_path, dpi=150)

plot.show()