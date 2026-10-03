from sec_data import download_data
from process_data import process_data
from plot_data import create_charts


def main():
    ticker = input("Ticker: ").strip().upper()

    if not ticker:
        raise ValueError("Enter a ticker, such as AAPL.")

    print(f"Downloading financial data for {ticker}...")
    download_data(ticker)

    print("Building annual summary...")
    summary_path = process_data(ticker)

    print(f"Creating charts in {summary_path.parent}...")
    create_charts(ticker, summary_path)

    print("Done.")


if __name__ == "__main__":
    main()