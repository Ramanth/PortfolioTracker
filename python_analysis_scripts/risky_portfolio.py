from utils import show_pl_with_current_price
# show_pl_with_current_price("2023-10-23 00:00:00", "2023-10-25 00:00:00")
import sqlite3
from datetime import datetime

# Function to create the 'super_portfolio' table
def create_sub_portfolio_table():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risky_portfolio (
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
    INSERT OR REPLACE INTO risky_portfolio (Stock, Quantity, AvgPrice)
    VALUES (?, ?, ?)
    ''', (stock, quantity, avg_price))
    connection.commit()
    connection.close()

# Function to update an existing record based on Stock name
def update_record(stock, new_quantity, new_avg_price):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE risky_portfolio
    SET Quantity = ?, AvgPrice = ?
    WHERE Stock = ?
    ''', (new_quantity, new_avg_price, stock))
    connection.commit()
    connection.close()

# Example usage:
create_sub_portfolio_table()
insert_record('INFOEDGE', 29, 4163)
insert_record('LICI', 48, 643)
insert_record('JUBLFOOD', 50, 523)
insert_record('BHEL', 200, 132)
insert_record('JSWSTEEL', 31, 784)
insert_record('CMSINFO', 50, 370)
insert_record('IOC', 150, 94)
# insert_record('NAM-INDIA', 150, 370)
# insert_record('AARTIDRUGS', 150, 509)
# insert_record('MEDPLUS', 0, 0)
# insert_record('VRLLOG', 0, 0)
# insert_record('EMAMILTD', 0, 0)
# update_record('AAPL', 150, 155.0)
