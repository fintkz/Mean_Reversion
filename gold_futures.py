import yfinance as yf
import pandas as pd

# Define the ticker symbol for gold futures
symbol = 'GC=F'

# Define the start and end dates for the data
start_date = '2021-01-01'
end_date = '2023-01-01'

# Fetch the data from Yahoo Finance API
df = yf.download(symbol, start=start_date, end=end_date)

# Extract the OHLC data from the DataFrame
df = df[['Open', 'High', 'Low', 'Close']]

# Print the DataFrame
print(df)
