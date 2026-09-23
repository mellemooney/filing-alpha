import json
from datetime import date
from pathlib import Path


ticker = "AAPL"



# finds prject folder a level above src
PROJECT_ROOT = Path(__file__).resolve().parents[1]

file_path = PROJECT_ROOT / "data" / "raw" / "companyFacts" / f"{ticker}_companyFacts.json"

with open(file_path, "r", encoding="utf-8") as file:
    company_data = json.load(file)

us_gaap = company_data["facts"]["us-gaap"]

net_income = us_gaap["NetIncomeLoss"]

records = net_income["units"]["USD"]



#finds all instances of annual records and print total amount found
annual_records = []

for record in records:
    if "start" not in record or "end" not in record:
        continue

    start = date.fromisoformat(record["start"])
    end = date.fromisoformat(record["end"])
    duration = (end - start).days

    if record["form"] == "10-K" and 350 <= duration <= 380:
        annual_records.append(record)



#sifts out duplicates by prioritizing the latest duplicate
latest_by_period = {}

for record in annual_records:
    period = (record["start"], record["end"])

    if period not in latest_by_period:
        latest_by_period[period] = record

    elif record["filed"] > latest_by_period[period]["filed"]:
        latest_by_period[period] = record




#sorts the remaining entries by end date
annual_net_income = sorted(
    latest_by_period.values(),
    key=lambda record: record["end"]
)
print(f"Found {len(annual_net_income)} annual records")


#
for i in range(len(annual_net_income)):
    net_income = annual_net_income[i]["val"]
    period_end = annual_net_income[i]["end"]

    if i == 0:
        print(f"{period_end} | {net_income:,.0f} | Growth: N/Ahh")
        continue

    previous_income = annual_net_income[i - 1]["val"]

    if previous_income <= 0:
        growth_text = "N/A"
    else:
        growth = (net_income - previous_income) / previous_income * 100

    print(
        f"{period_end} | {net_income:,.0f} | {growth:+.2f}%"
    )
