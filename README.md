# Sharpe Ratio Analyzer

This project is a Python-based evaluation framework that calculates and compares the risk-adjusted performance of multiple stocks using the Sharpe Ratio.

![Sharpe Ratio Comparison Plot](images/sharpe_plot.png)

## About This Project

The Sharpe Ratio is a core concept in modern portfolio theory that measures how much excess return an asset generates per unit of volatility risk. This tool helps investors determine which assets compensate them most efficiently for the risk they take on.

### Features
* Fetches up-to-date historical stock data from Yahoo Finance.
* Calculates the annualized Sharpe Ratio for any list of stock tickers.
* Uses the 13-week US Treasury Bill (`^IRX`) as a proxy for the risk-free rate.
* Generates a clean bar chart to visually compare the risk-adjusted performance of all assets.

---

## How to Use

### 1. Prerequisites
* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

### 2. Setup & Installation
Clone this repository and set up the virtual environment:

```bash
# 1. Clone the repository to your local machine
git clone [https://github.com/YourUsername/Sharpe-Ratio-Analyzer.git](https://github.com/YourUsername/Sharpe-Ratio-Analyzer.git)
cd Sharpe-Ratio-Analyzer

# 2. Create a Python virtual environment
python -m venv venv

# 3. Activate the environment
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 4. Install the required libraries
pip install -r requirements.txt
```
### 3. Running the Analyzer
You can customize the stocks and time period by editing the __main__ block at the bottom of the sharpe_analyzer.py file.

```bash
# --- Customize Your Inputs Here ---
stock_tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'JPM']
risk_free_rate_ticker = '^IRX'
start_date = '2020-01-01'
end_date = '2025-11-26'
```
Once customized, simply run the script from your terminal:
```bash
python sharpe_analyzer.py
```
The script will print the numerical results to the console and display the visual plot in a new window.