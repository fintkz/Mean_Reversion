# Mean Reversion Trading Strategy for Gold Futures

This project implements a simple mean reversion trading strategy for gold futures using simple Python libraries and the Yahoo Finance API.

Please note that this is a very simple project and is for educational purposes only and should not be used in production without thorough testing and analysis. Use at your own risk.

## Overview

The strategy is based on two moving averages (30-day and 90-day) of the daily closing price of gold futures. When the difference between the price and the moving averages falls below a fixed threshold, the strategy generates a buy signal. When the difference rises above another fixed threshold, it generates a sell signal.

The strategy also includes a stop loss rule to limit downside risk. If the price falls below a certain percentage of the previous day's closing price, any open position is closed.

## Results

Using historical data from January 1, 2021 to January 1, 2023, the strategy generated a total return of $7577.40, equivalent to a percentage return of 7.58%. The strategy generated a total of 18 trades, with 8 wins and 1 loss.

## How to Use

To run the strategy, clone this repository and run the `mean_reversion_strategy.py` script. For backtesting and generating the trading signal chart run the `gold_futures_meanReversion_backtest.py` script. The scripts require the `yfinance`, `pandas`, and `matplotlib` libraries, which can be installed using "pip install -r requirements.txt".

