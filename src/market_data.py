import yfinance as yf
from pathlib import Path

#definitons
def get_market_data(ticker):
    ticker = ticker.upper()
    market_data = yf.download(ticker, 
        start = "2015-01-01",
        #end = "year-month-day",
        auto_adjust=False)

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    output_folder = PROJECT_ROOT / "data" / "raw" / "marketData"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{ticker}_marketData.csv"

    market_data.to_csv(output_path)

ticker = input("Enter Ticker: ")
get_market_data(ticker)
