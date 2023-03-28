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

    return df

# Fetch the data from Yahoo Finance API
df = yf.download(symbol, start=start_date, end=end_date)

# Extract the OHLC data from the DataFrame
df = df[['Open', 'High', 'Low', 'Close']]

# Generate the trading signal based on the mean reversion strategy
df = generate_signal(df)

# Plot the mean reversion and trading signals
fig, ax = plt.subplots(figsize=(10,5))

# Plot the OHLC data
ax.plot(df.index, df['Close'], label='Close', color='black')
ax.fill_between(df.index, df['Low'], df['High'], alpha=0.2, label='Range', color='grey')

# Plot the moving averages
df_mean_30 = df['Close'].rolling(window=30).mean()
df_mean_90 = df['Close'].rolling(window=90).mean()
ax.plot(df_mean_30.index, df_mean_30, label='30-day Moving Average', color='blue')
ax.plot(df_mean_90.index, df_mean_90, label='90-day Moving Average', color='green')

# Plot the trading signals
ax.plot(df[df['Signal'] == 1].index, df[df['Signal'] == 1]['Close'], marker='^', markersize=10, color='green', label='Buy')
ax.plot(df[df['Signal'] == -1].index, df[df['Signal'] == -1]['Close'], marker='v', markersize=10, color='red', label='Sell')

# Add plot labels and legend
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title(f'{symbol} Mean Reversion Trading Strategy')
ax.legend()

# Save the plot to a file
fig.savefig('trading_signal.svg', format='svg', dpi=1200)

# Display the plot
plt.show()
