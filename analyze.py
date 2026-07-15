import pandas as pd
from sqlalchemy import create_engine

# 1. Establish Database Connection
DATABASE_URL = "postgresql://admin:supersecretpassword@localhost:5432/stock_data"
engine = create_engine(DATABASE_URL)

# 2. Define all our analytical queries in a dictionary
queries = {
    "1. Moving Average (Golden Cross Trend)": """
        SELECT 
            timestamp,
            close,
            ROUND(AVG(close) OVER(ORDER BY timestamp ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)::numeric, 2) as rolling_5_period_avg
        FROM raw_stock_prices
        ORDER BY timestamp DESC
        LIMIT 5;
    """,
    
    "2. Data Integrity Audit (Duplicate Check)": """
        SELECT 
            timestamp, 
            symbol, 
            COUNT(*) as record_count
        FROM raw_stock_prices
        GROUP BY timestamp, symbol
        HAVING COUNT(*) > 1;
    """,
    
    "3. Financial Capital Flow (Cumulative)": """
        SELECT 
            DATE(timestamp) as trade_date,
            ROUND(SUM(volume * close)::numeric, 2) as daily_capital_flow,
            ROUND(SUM(SUM(volume * close)) OVER(ORDER BY DATE(timestamp))::numeric, 2) as cumulative_capital_flow
        FROM raw_stock_prices
        GROUP BY trade_date
        ORDER BY trade_date DESC
        LIMIT 5;
    """,
    
    "4. Market Extreme Peak (Highest Volatility)": """
        SELECT 
            timestamp,
            high,
            low,
            ROUND((high - low)::numeric, 2) as spread,
            ROUND(((high - low) / low * 100)::numeric, 2) as percent_volatility
        FROM raw_stock_prices
        ORDER BY spread DESC
        LIMIT 1;
    """
}

# 3. Loop through and run each query
print("=" * 60)
print("             ENTERPRISE FINANCIAL INTELLIGENCE REPORT         ")
print("=" * 60)

for title, sql in queries.items():
    print(f"\n★ Running: {title}")
    print("-" * 60)
    
    try:
        # Execute the query and load it into a Pandas DataFrame
        df = pd.read_sql(sql, engine)
        
        # If the dataframe is empty, let the user know cleanly (especially for the duplicate check!)
        if df.empty:
            print("   [INFO] No records found / Audit passed successfully! ✅")
        else:
            print(df.to_string(index=False))
            
    except Exception as e:
        print(f"   [ERROR] Failed to execute query: {e}")
        
    print("-" * 60)

print("\n" + "=" * 60)
print("                       END OF REPORT                          ")
print("=" * 60)