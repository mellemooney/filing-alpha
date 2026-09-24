#imports
import requests, json
from pathlib import Path

#contants
headers = {
        "User-Agent": "FilingAlpha : meadowsnull@gmail.com",
    }

#definitions

#get_cik looks up a companys cik(cCentral Index Key) using its ticker symbol
#by retrieiving the SEC's ticker to CIK map and searching for the requested ticker
#returns the companys 10 digit CIK padded by leading zeros
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


#download_company_facts uses the SEC's EDGAR API to retrieve financial facts for the given cik argument
#ticker is passed as an argument for the file naming portion of the code
#the data is parsed from json and stores as a dict
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
    output_folder = PROJECT_ROOT / "data" / "raw" / "companyFacts"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{ticker}_companyFacts.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, indent=2)
    

ticker = input("Enter Ticker: ")
download_company_facts(get_cik(ticker,headers),headers,ticker)


