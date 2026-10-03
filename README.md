# Filing Alpha - V 0.1

- A python project that turns Apple's SEC financial data into annual and financial summary and charts using SEC data.

- Filing Alpha converts raw financial observations into a five-period summary, a CSV export, and charts. The project focuses on matching reporting periods, resolving repeated observations, and keeping results traceable to their source filings.

Example

![Apple annual revenue](docs/images/AAPL_revenue.png)

![Apple profit margins](docs/images/AAPL_margins.png)

## Features

- Downloads financial facts from the SEC Company Facts API.

- Extracts annual revenue, operating income, and net income.

- Selects the most recently filed observation for each financial period.

- Calculates operating margin, net margin, and year-over-year revenue growth.

- Exports a CSV containing financial values, calculated metrics, and source accession numbers.

- Generates revenue and profit-margin charts.

## Setup -  The instructions use windows powershell and python 3.11

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    python -m pip install -r requirements.txt

    Copy-Item .env.example .env

- Before downloading SEC data, update the SEC_CONTACT_EMAIL value in the .env with your email.
- The download script includes this email in its SEC request header.

Start
- Download Apple's Financial Data, when prompted enter "AAPL" for all input requests
    ```
    python src/sec_data.py
    ```
    
- Build the Annual Summary
    ```
    python src/process_data.py
    ```
- Generate Charts
    ```
    python src/plot_data.py
    ```
    The downloader, processing and plotting scripts accepts other tickers, but their compatibility with the analysis is not guaranteed.

Additional Script

- src/market_data.py downloads historical stock prices using yfinance. It is separate from the financial analysis and is not required to generate the summary or charts.

Generated Files

- Downloaded data and generated results are excluded from Git. The images in docs/images are saved examples; running the scripts does not update those copies.

- The CSV contains reporting dates, financial values in USD, margins, revenue growth, and source accession numbers. Percentage values use percentage units: 6.43 means 6.43%.

Scope and limitations

- I built this version around Apple’s financial data. Other companies may use different financial tags, so changing the ticker alone might not work.

- The code looks for annual records covering 350–380 days. This works for the Apple data used here, but may need adjustments for other reporting periods.

- If matching revenue or income data is missing, that period is skipped, so the output may contain fewer than five years.

- For each metric, the code keeps the most recently filed value available in the downloaded data. It also saves the filing identifier so the source can be checked.

- Downloading newer filings may change the results if earlier figures have been updated.

- This project looks at historical financial performance. It does not predict stock prices or recreate exactly what information was available to investors at a past date.

Tools

- Python, Requests, python-dotenv, Matplotlib, and Python’s built-in JSON and CSV modules. The optional market_data script uses yfinance.