import json, csv
from datetime import date
from pathlib import Path





#############
#Definitions#
#############

#get_annual_records:
#takes in us_gaap for a given company and then finds a specific metric(metric_tag)
#within the us_gaap dict and returns all annual records after removing duplicates and 
#sorting by end date, oldest first, newest last
def get_annual_records(us_gaap, metric_tag):
    records = us_gaap[metric_tag]["units"]["USD"]

    annual_records = []

    for record in records:
        if "start" not in record or "end" not in record:
            continue

        start = date.fromisoformat(record["start"])
        end = date.fromisoformat(record["end"])
        duration = (end - start).days

        if record["form"] == "10-K" and 350 <= duration <= 380:
            annual_records.append(record)


    latest_by_period = {}

    for record in annual_records:
        period = (record["start"], record["end"])

        if period not in latest_by_period:
            latest_by_period[period] = record

        elif record["filed"] > latest_by_period[period]["filed"]:
            latest_by_period[period] = record

    return sorted(
        latest_by_period.values(),
        key=lambda record: record["end"]
    )



#index_by_period:
#takes the list of records and indexes them by period 
#(this function does seem a bit redundant since the 'latest_by_period' in the 'get_annual_records' function
#is already keyed by period however in wanting tha function to return a single sorted list and not having
#foreseen the need for this later on i am willing to leave it considering my datset is small)
def index_by_period(records):
    by_period = {}
    for record in records:
        period = (record['start'], record['end'])
        by_period[period] = record
    return by_period



#year_to_year_change
#
def year_to_year_change(records):
    for i in range(len(records)):
        current = records[i]['val']
        period_end = records[i]['end']

        if i == 0:
            print(f"{period_end} | {current:,.0f} | Growth: N/A")
            continue

        previous = records[i - 1]['val']

        if previous <= 0:
            growth_text = "N/A"
        else:
            growth = (current - previous) / previous * 100
            growth_text = f"{growth:+.2f}%"

        print(
            f"{period_end} | {current:,.0f} | Growth: {growth_text}"
        )



#
#
def build_profit_margins(
    annual_net_income,
    revenue_by_period,
    operating_income__by_period
):
    results = []

    for record in annual_net_income[-5:]:
        period = (record["start"], record["end"])

        if period not in revenue_by_period or period not in operating_income__by_period:
            print(f"{record['end']} | Missing matching data")
            continue

        net_income = record['val']
        revenue = revenue_by_period[period]['val']
        operating_income = operating_income__by_period[period]['val']

        if revenue <= 0:
            print(f"{record['end']} | Margins unavailable")
            continue

        operating_margin = operating_income / revenue * 100
        net_margin = net_income / revenue * 100

        row = {
            "start": record['start'],
            "end": record['end'],
            "revenue": revenue,
            "operating income": operating_income,
            "net income": net_income,
            "operating margin pct": operating_margin,
            "net margin pct": net_margin,
        }

        results.append(row)

        #print(
        #    f"{record['end']} | "
        #    f"Operating margin: {operating_margin:.2f}% | "
        #    f"Net margin: {net_margin:.2f}%")
    
    return results



#
#
def save_to_csv(summary,output_path):
    output_path.parent.mkdir(parents=True,exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(summary[0].keys())
        )

        writer.writeheader()
        writer.writerows(summary)



######
#CODE#
######

ticker = "AAPL"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

file_path = PROJECT_ROOT / "data" / "raw" / "companyFacts" / f"{ticker}_companyFacts.json"

output_path = PROJECT_ROOT / "data" / "processed" / f"{ticker}_annual_summary.csv"

with open(file_path, "r", encoding="utf-8") as file:
    company_data = json.load(file)

us_gaap = company_data["facts"]["us-gaap"]


annual_net_income = get_annual_records(
    us_gaap,
    "NetIncomeLoss"
)
income_by_period = index_by_period(annual_net_income)

annual_revenue = get_annual_records(
    us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)
revenue_by_period = index_by_period(annual_revenue)

annual_operating_income = get_annual_records(
    us_gaap,
    "OperatingIncomeLoss"
)
operating_income__by_period = index_by_period(annual_operating_income)


summary = (build_profit_margins(annual_net_income,revenue_by_period,operating_income__by_period))

save_to_csv(summary,output_path)

