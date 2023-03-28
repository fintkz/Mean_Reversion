import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the ticker symbol for gold futures
symbol = 'GC=F'

# Define the start and end dates for the data
start_date = '2021-01-01'
end_date = '2023-01-01'

# Define the trading signal parameters (assuming a simple strategy with fixed thresholds)
buy_threshold = -2  # buy when the difference between price and moving average is below this value
sell_threshold = 2  # sell when the difference between price and moving average is above this value
stop_loss = 0.05    # stop loss percentage to limit downside risk

# Define the function to generate the trading signal
def generate_signal(df):
    # Calculate the 30-day and 90-day moving averages of the OHLC data
    df_mean_30 = df['Close'].rolling(window=30).mean()
    df_mean_90 = df['Close'].rolling(window=90).mean()

    # Calculate the difference between the OHLC data and the moving averages
    df_diff_30 = df['Close'] - df_mean_30
    df_diff_90 = df['Close'] - df_mean_90

    # Initialize the signal column to hold the trading signals
    df.loc[:, 'Signal'] = 0

    # Generate the trading signals based on the mean reversion strategy
    for i in range(1, len(df)):
        if df_diff_30[i] < buy_threshold and df_diff_90[i] < buy_threshold:
            df.at[df.index[i], 'Signal'] = 1  # buy signal
        elif df_diff_30[i] > sell_threshold and df_diff_90[i] > sell_threshold:
            df.at[df.index[i], 'Signal'] = -1  # sell signal

        # Apply the stop loss rule
        if df.at[df.index[i], 'Signal'] == 1:
            if df['Close'][i] < (1 - stop_loss) * df['Close'][df.index[i-1]]:
                df.at[df.index[i], 'Signal'] = 0  # stop loss triggered

    return df, df_mean_30, df_mean_90

# Fetch the data from Yahoo Finance API
df = yf.download(symbol, start=start_date, end=end_date)

# Extract the OHLC data from the DataFrame
df = df[['Open', 'High', 'Low', 'Close']]

# Generate the trading signal based on the mean reversion strategy
df, df_mean_30, df_mean_90  = generate_signal(df)

# Backtest the trading signal
capital = 100000
shares = 0
wins = 0
losses = 0
total_trades = 0
trade_data = []
avg_price = 0

for i in range(1, len(df)):
    # Buy signal
    if df.at[df.index[i], 'Signal'] == 1:
        shares_to_buy = int(capital / df['Close'][i])
        if shares_to_buy > 0:
            shares += shares_to_buy
            capital -= shares_to_buy * df['Close'][i]
            avg_price = (avg_price * (shares - shares_to_buy) + shares_to_buy * df['Close'][i]) / shares
            total_trades += 1
            trade_data.append(('buy', df.index[i], df['Close'][i], shares_to_buy))
    # Sell signal
    elif df.at[df.index[i], 'Signal'] == -1:
        if shares > 0:
            shares_to_sell = shares
            shares = 0
            capital += shares_to_sell * df['Close'][i]
            pl = shares_to_sell * (df['Close'][i] - avg_price)
            if pl > 0:
                wins += 1
            elif pl < 0:
                losses += 1
            total_trades += 1
            trade_data.append(('sell', df.index[i], df['Close'][i], shares_to_sell))

# Calculate the total return and the percentage return
total_return = capital - 100000
pct_return = total_return / 1000

# Print the backtesting results
print(f'Total return: ${total_return:.2f}')
print(f'Percentage return: {pct_return:.2f}%')
print(f'Total trades: {total_trades}')
print(f'Wins: {wins}')
print(f'Losses: {losses}')

# Plot the closing price and the moving averages
plt.figure(figsize=(12,6))
plt.plot(df.index, df['Close'], label='Close')
plt.plot(df_mean_30.index, df_mean_30, label='30-day moving average')
plt.plot(df_mean_90.index, df_mean_90, label='90-day moving average')
plt.legend()
plt.title('Gold Futures Mean Reversion Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
