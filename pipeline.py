import requests
import pandas as pd
from sqlalchemy import create_engine
import datetime

# 1. FETCH DATA (Using a free public API for mock stock prices)
print("Fetching live stock prices...")
url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
# Yahoo Finance requires a User-Agent header so they don't block us
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

data = response.json()

# 2. EXTRACT & CLEAN DATA using Pandas
print("Processing data...")
result = data['chart']['result'][0]
timestamps = result['timestamp']
indicators = result['indicators']['quote'][0]

# Create a clean tabular format
df = pd.DataFrame({
    'timestamp': [datetime.datetime.fromtimestamp(ts) for ts in timestamps],
    'symbol': 'AAPL',
    'open': indicators['open'],
    'high': indicators['high'],
    'low': indicators['low'],
    'close': indicators['close'],
    'volume': indicators['volume']
})

# Drop rows that have missing values
df = df.dropna()

# 3. LOAD DATA TO POSTGRESQL
print("Connecting to database and writing data...")
# Database URL format: postgresql://username:password@host:port/database_name
DATABASE_URL = "postgresql://admin:supersecretpassword@localhost:5432/stock_data"
engine = create_engine(DATABASE_URL)

# Write to a table named 'raw_stock_prices'. If it exists, append new data.
df.to_sql('raw_stock_prices', engine, if_exists='append', index=False)
print("Data successfully loaded into PostgreSQL! 🚀")