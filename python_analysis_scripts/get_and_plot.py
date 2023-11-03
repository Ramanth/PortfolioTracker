import sqlite3
import matplotlib.pyplot as plt
import pandas as pd


def get_unique_stock_names_from_database():
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")  # Replace "your_database.db" with your database file path
    # Create a cursor object
    cursor = conn.cursor()
    # Execute a query to retrieve unique stock names
    cursor.execute("SELECT DISTINCT Stock FROM price_changes_10_23")
    # Fetch all the unique stock names
    unique_stock_names = cursor.fetchall()
    # Close the database connection
    conn.close()
    # Return the unique stock names as a list
    return [name[0] for name in unique_stock_names]

def plot_price(symbol):
    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')  # Replace 'your_database.db' with your database file name
    cursor = conn.cursor()

    # Specify the stock you want to retrieve data for
    stock_symbol = symbol  # Replace with the desired stock symbol

    # Fetch data for the specified stock
    cursor.execute('SELECT DateTime, Price FROM price_changes_10_23 WHERE stock = ?', (stock_symbol,))
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data to a DataFrame for easier handling
    df = pd.DataFrame(data, columns=['datetime', 'price'])
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df['price'], label=f'{stock_symbol} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{stock_symbol} Stock Price Over Time')
    plt.legend()
    plt.grid()

    # Show the plot
    plt.tight_layout()
    plt.show()

stock_names = get_unique_stock_names_from_database()

for each_stock in stock_names:
    plot_price(each_stock)
