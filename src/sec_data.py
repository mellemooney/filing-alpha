#imports
import requests, json
from pathlib import Path

#contants
headers = {
        "User-Agent": "FilingAlpha : meadowsnull@gmail.com",
    }

#definitions
def get_cik(ticker,headers):
    ticker = ticker.upper()
    response = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
    )
    response.raise_for_status()

    ticker_data = response.json()

    for company in ticker_data.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            #company_name = company["title"]
            return cik #, company_name
    raise ValueError(f"ticker '{ticker}' not found")



def download_company_facts(cik,headers,ticker):
    ticker = ticker.upper()
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(
            url,
            headers=headers
            )
    response.raise_for_status()

    raw_data = response.json()
    

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    output_folder = PROJECT_ROOT / "data" / "raw"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{ticker}_companyfacts.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, indent=2)
    


download_company_facts(get_cik("AAPL",headers),headers,"AAPL")



