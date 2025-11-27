import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_sharpe_ratios(tickers, risk_free_ticker, start_date, end_date):
    """
    Analyzes and calculates the annualized Sharpe Ratios for a portfolio of assets.

    The Sharpe Ratio is a measure of risk-adjusted return, defined as
    (Mean Asset Return - Mean Risk-Free Return) / Std Dev of Excess Return.

    Args:
        tickers (list): A list of asset ticker symbols (e.g., ['AAPL', 'MSFT']).
        risk_free_ticker (str): The ticker for the risk-free rate proxy
                                (e.g., '^IRX' for 13-week T-bill).
        start_date (str): The start date for historical data in 'YYYY-MM-DD' format.
        end_date (str): The end date for historical data in 'YYYY-MM-DD' format.

    Returns:
        pandas.Series: A Series of calculated annualized Sharpe Ratios, indexed by ticker.
    """
    
    # 1. Retrieve Historical Market Data
    # Consolidate tickers for a single, efficient API call
    tickers_with_rf = tickers + [risk_free_ticker]
    try:
        # Download 'Close' prices. With yfinance's new default (auto_adjust=True),
        # 'Close' is already the adjusted close price.
        data = yf.download(tickers_with_rf, start=start_date, end=end_date)['Close'] # <-- THIS IS THE FIX
        
        if data.empty:
            print("Error: No data downloaded. Verify tickers and date range.")
            return None
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

    # 2. Compute Daily Percentage Returns
    # pct_change() calculates the daily price movement
    returns = data.pct_change().dropna()

    # 3. Isolate Asset Returns and Risk-Free Rate
    stock_returns = returns[tickers]
    
    # Normalize the risk-free rate:
    # T-bill yield ('^IRX') is an annualized percentage (e.g., 5.25).
    # We must convert it to a daily decimal representation for calculations.
    rf_daily = returns[risk_free_ticker] / 100 / 252
    
    # 4. Compute Daily Excess Returns
    # Excess return is the asset's return minus the risk-free rate.
    # This represents the reward for taking on additional risk.
    # .subtract(axis=0) correctly aligns the daily risk-free rate with each asset's return column.
    excess_returns = stock_returns.subtract(rf_daily, axis=0)

    # 5. Calculate Key Statistics for Excess Returns
    # mean_excess_returns: The average daily excess return (the "reward")
    mean_excess_returns = excess_returns.mean()
    
    # std_excess_returns: The standard deviation of daily excess return (the "risk" or "volatility")
    std_excess_returns = excess_returns.std()

    # 6. Compute the Daily Sharpe Ratio
    # This is the core formula: Reward / Risk
    daily_sharpe_ratio = mean_excess_returns / std_excess_returns

    # 7. Annualize the Sharpe Ratio for Reporting
    # We scale the daily ratio to an annual equivalent by multiplying
    # by the square root of the number of trading days (approx. 252).
    annualized_sharpe_ratio = daily_sharpe_ratio * np.sqrt(252)

    return annualized_sharpe_ratio

def plot_sharpe_comparison(sharpe_ratios):
    """
    Generates a bar chart to visually compare the calculated Sharpe Ratios.

    Args:
        sharpe_ratios (pandas.Series): The annualized Sharpe Ratios from get_sharpe_ratios().
    """
    if sharpe_ratios is None or sharpe_ratios.empty:
        print("Plotting skipped: No Sharpe Ratios to display.")
        return

    # Dynamically set bar colors: green for positive (favorable) ratios, red for negative
    colors = ['g' if x > 0 else 'r' for x in sharpe_ratios]
    
    # Initialize the plot figure
    plt.figure(figsize=(10, 6))
    
    # Generate the bar plot
    sharpe_ratios.plot(kind='bar', color=colors, rot=0)
    
    # Set plot titles and axis labels for clarity
    plt.title('Annualized Sharpe Ratio Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Asset Tickers', fontsize=12)
    plt.ylabel('Annualized Sharpe Ratio (Risk-Adjusted Return)', fontsize=12)
    
    # Add a zero-line benchmark to distinguish positive/negative performance
    plt.axhline(0, color='grey', linestyle='--')
    
    # Apply a light grid for improved readability of ratio values
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    
    # Annotate each bar with its precise Sharpe Ratio value
    for i, val in enumerate(sharpe_ratios):
        # Position text slightly above/below the bar
        y_pos = val + (0.05 * np.sign(val))
        va_align = 'bottom' if val > 0 else 'top'
        plt.text(i, y_pos, f'{val:.2f}', ha='center', va=va_align)

    # Ensure all elements fit within the figure
    plt.tight_layout()
    
    # Render the finalized plot to the screen
    print("\nDisplaying visual comparison chart...")
    plt.show()

# --- Script Execution Block ---
if __name__ == "__main__":
    
    # --- Configuration Parameters ---
    
    # 1. Asset Tickers: Define the assets to include in the analysis.
    stock_tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'JPM']
    
    # 2. Risk-Free Rate Proxy: Ticker for the benchmark risk-free asset.
    # Note: ^IRX (13-Week T-Bill) is a common proxy for the US risk-free rate.
    risk_free_rate_ticker = '^IRX'
    # 3. Analysis Period: Define the historical date range.
    start_date = '2020-01-01'
    # Note: Set end_date to a recent date to ensure data availability.
    end_date = '2025-11-26' 
    
    # --- End of Configuration ---

    print(f"Initializing Sharpe Ratio analysis for: {', '.join(stock_tickers)}")
    print(f"Data Period: {start_date} to {end_date}\n")

    # Execute the Sharpe Ratio calculation
    sharpe_ratios = get_sharpe_ratios(stock_tickers, risk_free_rate_ticker, start_date, end_date)

    if sharpe_ratios is not None:
        # Sort values for a cleaner presentation
        sorted_ratios = sharpe_ratios.sort_values(ascending=False)
        
        # Display numerical results in the console
        print("--- Analysis Results (Annualized Sharpe Ratio) ---")
        print(sorted_ratios)
        
        # Generate and display the comparative bar chart
        plot_sharpe_comparison(sorted_ratios)