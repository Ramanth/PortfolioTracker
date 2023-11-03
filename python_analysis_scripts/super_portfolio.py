from utils import show_pl_with_current_price
# show_pl_with_current_price("2023-10-23 00:00:00", "2023-10-25 00:00:00")
import sqlite3
from datetime import datetime
import sqlite3
import pandas as pd

# Function to create the 'super_portfolio' table
def create_super_portfolio_table():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS super_portfolio (
        Stock TEXT PRIMARY KEY,
        Quantity INTEGER,
        AvgPrice REAL,
        DateTime TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    connection.commit()
    connection.close()

# Function to insert a new record into the 'super_portfolio' table
def insert_record(stock, quantity, avg_price):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO super_portfolio (Stock, Quantity, AvgPrice)
    VALUES (?, ?, ?)
    ''', (stock, quantity, avg_price))
    connection.commit()
    connection.close()

# Function to update an existing record based on Stock name
def update_record(stock, new_quantity, new_avg_price):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE super_portfolio
    SET Quantity = ?, AvgPrice = ?
    WHERE Stock = ?
    ''', (new_quantity, new_avg_price, stock))
    connection.commit()
    connection.close()




def calculate_profit_loss_of_portfolio(portfolio_name):
    # Provide the path to your SQLite database
    database_path = 'my_database.db'
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    # Query data from the 'super_portfolio' table
    query = "SELECT * FROM " + portfolio_name
    super_portfolio_df = pd.read_sql_query(query, conn)
    # Query data from the 'current_price' table
    query = "SELECT * FROM current_price"
    current_price_df = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    # Merge the dataframes on the 'Stock' column
    merged_df = super_portfolio_df.merge(current_price_df, on='Stock', how='left')
    # Calculate the profit/loss for each row
    merged_df['price_diff'] = (merged_df['price'] - merged_df['AvgPrice'])
    merged_df['price_diff_percent'] = merged_df['price_diff']/merged_df['AvgPrice'] * 100
    merged_df['Profit_Loss'] = merged_df['price_diff'] * merged_df['Quantity']
    merged_df['Invested'] = merged_df['AvgPrice'] * merged_df['Quantity']
    merged_df['20% price'] = (merged_df['AvgPrice'] + merged_df['AvgPrice']*0.2)
    merged_df['If20% growth'] = ((merged_df['AvgPrice'] + merged_df['AvgPrice']*0.2)* merged_df['Quantity']) - merged_df['Invested']
    return merged_df





# Example usage:
# create_super_portfolio_table()
# insert_record('INFY', 75, 1415)
# update_record('AAPL', 150, 155.0)
