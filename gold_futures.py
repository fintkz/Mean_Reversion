import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the ticker symbol for gold futures
symbol = 'GC=F'

# Define the start and end dates for the data
start_date = '2021-01-01'
end_date = '2023-01-01'

# Fetch the data from Yahoo Finance API
df = yf.download(symbol, start=start_date, end=end_date)

# Extract the OHLC data from the DataFrame
df = df[['Open', 'High', 'Low', 'Close']]

# Calculate the 30-day moving average of the OHLC data
df_mean = df.rolling(window=30).mean()

# Calculate the difference between the OHLC data and the moving average
df_diff = df.subtract(df_mean, axis=0)

# Plot the mean reversion
plt.figure(figsize=(10,5))
plt.plot(df_diff)
plt.axhline(y=0, color='black', linestyle='--')
plt.title(f'Mean Reversion of {symbol} from {start_date} to {end_date} (30-day Moving Average)')
plt.xlabel('Date')
plt.ylabel('Difference')
plt.savefig('mean_reversion_ma.png', dpi=300)

# Show the plot
plt.show()

# Save the DataFrame to a CSV file
df.to_csv('gold_futures_OLHC.csv', index=True)
