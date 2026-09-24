#imports
import yfinance as yf
from pathlib import Path

#definitons

#get_market_data takes in a ticker symbol and using yfinance library 
#retrieves OHLC and volume data from 2015 to the present in csv format
#downloads the data at data/raw/marketData
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
