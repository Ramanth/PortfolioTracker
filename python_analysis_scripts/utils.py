import sqlite3
import pandas as pd

def get_transactions():
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")
    # Define the date you want to match
    date_to_match = "2023-10-23 00:00:00"
    # Construct the SQL query to select records with a specific date
    query = f"SELECT * FROM transactions WHERE Datetime = '{date_to_match}'"
    # Use pandas to read the result of the SQL query into a DataFrame
    df = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    return df

def get_unique_stock_names_from_transactions():
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")  # Replace "your_database.db" with your database file path
    # Create a cursor object
    cursor = conn.cursor()
    # Execute a query to retrieve unique stock names
    cursor.execute("SELECT DISTINCT Stock FROM transactions")
    # Fetch all the unique stock names
    unique_stock_names = cursor.fetchall()
    # Close the database connection
    conn.close()
    # Return the unique stock names as a list
    return [name[0] for name in unique_stock_names]

def get_current_price(stock):
    conn = sqlite3.connect("my_database.db")
    query = f"SELECT * FROM current_price WHERE Stock = '{stock}'"
    result = conn.execute(query)
    record = result.fetchone()
    if(record):
        return record[1]
    else:
        return 0

get_current_price("IIFLSEC")
def show_net_pl_using_transactions(from_date, to_date):
    total_pl = 0
    positive_pl = 0
    negative_pl=0
    stock_names = get_unique_stock_names_from_transactions()
    data = []
    for symbol in stock_names:
        
        conn = sqlite3.connect("my_database.db")
        buy_query = f"SELECT * FROM transactions WHERE Side = 'Buy' AND Stock = '{symbol}' AND Datetime BETWEEN '{from_date}' AND '{to_date}'"
        buy_df = pd.read_sql_query(buy_query, conn)
        buy_df['Inv'] = buy_df['Price'] * buy_df['Quantity']
        buy_tx_avg_price = 0
        if buy_df['Quantity'].sum() > 0 :
            buy_tx_avg_price = buy_df['Inv'].sum()/buy_df['Quantity'].sum()
        buy_tx_total_qty = buy_df['Quantity'].sum()


        sell_query = f"SELECT * FROM transactions WHERE Side = 'Sell' AND Stock = '{symbol}' AND Datetime BETWEEN '{from_date}' AND '{to_date}'"
        sell_df = pd.read_sql_query(sell_query, conn)
        sell_df['Inv'] = sell_df['Price'] * sell_df['Quantity']
        sell_tx_avg_price = 0
        if sell_df['Quantity'].sum() > 0:
            sell_tx_avg_price = sell_df['Inv'].sum()/sell_df['Quantity'].sum()
        sell_tx_total_qty = sell_df['Quantity'].sum()

        current_price = get_current_price(symbol)

        if(buy_tx_total_qty >= sell_tx_total_qty):
            pl = int((sell_tx_avg_price - buy_tx_avg_price)* sell_tx_total_qty)
            total_pl = total_pl + pl
            if pl < 0 :
                negative_pl = negative_pl + pl
            else:
                remaining_stocks = int(buy_tx_total_qty - sell_tx_total_qty)
                positive_pl = positive_pl + pl
                unrealized_pl = "Dont Know"
                if(current_price != 0):
                    unrealized_pl = int(remaining_stocks * (current_price - buy_tx_avg_price))
            data.append({'Stock': symbol, 'RealizedPL':str(pl), 'Remaining': str(remaining_stocks), "UnrealizedPL":str(unrealized_pl)})
        else:
            pl = int((sell_tx_avg_price - buy_tx_avg_price)* buy_tx_total_qty)
            total_pl = total_pl + pl
            if pl < 0 :
                negative_pl = negative_pl + pl
            else:
                positive_pl = positive_pl + pl
            data.append({'Stock': symbol, 'RealizedPL':str(pl), 'Remaining': 'Dont Know'})
    df = pd.DataFrame(data)
    print(df)
    print("Total Pl: " + str(total_pl))
    print("Postive Pl: " + str(positive_pl))
    print("Negative Pl: " + str(negative_pl))

# show_net_pl_using_transactions("2023-10-23 00:00:00", "2023-11-01 00:00:00")
# day_datetime = "2023-10-23 00:00:00"

def show_pl_with_current_price(from_date, to_date):
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")
    # Define the date you want to retrieve transactions for
    date_to_match = "2023-10-23 00:00:00"
    # Retrieve transactions data for the specified date
    transactions_query = f"SELECT * FROM transactions WHERE Side = 'Buy' AND Datetime = '{date_to_match}'"
    transactions_query = f"SELECT * FROM transactions WHERE Side = 'Buy' AND Datetime BETWEEN '{from_date}' AND '{to_date}'"
    transactions_df = pd.read_sql_query(transactions_query, conn)
    # Retrieve current price data
    current_price_query = "SELECT * FROM current_price"
    current_price_df = pd.read_sql_query(current_price_query, conn)
    # Merge the transactions and current price dataframes on the 'stock' column
    combined_df = pd.merge(transactions_df, current_price_df, on='Stock', how='inner')
    # Calculate profit or loss and add it as a new column 'profit_loss'
    combined_df['profit_loss'] = combined_df['Quantity'] * (combined_df['price'] - combined_df['Price'])
    combined_df['invested'] = combined_df['Quantity'] * (combined_df['Price'])
    # Print the resulting DataFrame
    print(combined_df)
    positive_pf = combined_df[combined_df['profit_loss'] >= 0]['profit_loss'].sum()
    negative_pf = combined_df[combined_df['profit_loss'] < 0]['profit_loss'].sum()
    print("Total PL: " + str(int(combined_df['profit_loss'].sum())))
    print("Postive PL: "+ str(int(positive_pf)))
    print("Negative PL: "+ str(int(negative_pf)))
    # Close the database connection
    print("\n")


    transactions_query = f"SELECT * FROM transactions WHERE Side = 'Sell' AND Datetime BETWEEN '{from_date}' AND '{to_date}'"
    transactions_df = pd.read_sql_query(transactions_query, conn)
    combined_df = pd.merge(transactions_df, current_price_df, on='Stock', how='inner')
    combined_df['missed_profit_loss'] = combined_df['Quantity'] * (combined_df['price'] - combined_df['Price'])
    print(combined_df)
    positive_pf = combined_df[combined_df['missed_profit_loss'] >= 0]['missed_profit_loss'].sum()
    negative_pf = combined_df[combined_df['missed_profit_loss'] < 0]['missed_profit_loss'].sum()
    print("Missed Profit: "+ str(int(positive_pf)))
    print("Missed Loss: "+ str(int(negative_pf)))
    conn.close()




