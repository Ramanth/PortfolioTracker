import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def plot_stock_data(stock_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')

    # Retrieve price change data for the given stock
    price_query = f"SELECT DateTime, Price FROM price_changes_10_23 WHERE Stock = ? ORDER BY DateTime"
    price_df = pd.read_sql_query(price_query, conn, params=(stock_name,))
    price_df['DateTime'] = pd.to_datetime(price_df['DateTime'])

    # Retrieve buy/sell transaction data for the given stock
    transaction_query = f"SELECT DateTime, Side, Price, Quantity FROM transactions WHERE Stock = ? ORDER BY DateTime"
    transaction_df = pd.read_sql_query(transaction_query, conn, params=(stock_name,))
    transaction_df['DateTime'] = pd.to_datetime(transaction_df['Datetime'])

    conn.close()

    # Merge and sort the data by DateTime
    merged_data = pd.concat([price_df, transaction_df])
    merged_data = merged_data.sort_values(by='DateTime')

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the price changes over time
    ax.plot(merged_data['DateTime'], merged_data['Price'], label=f'{stock_name} Price', color='b', linewidth=1)

    # Plot markers for buy and sell transactions on the timeline
    buy_indices = merged_data['Side'] == 'Buy'
    sell_indices = merged_data['Side'] == 'Sell'

    ax.scatter(merged_data.loc[buy_indices, 'DateTime'], merged_data.loc[buy_indices, 'Price'], marker='^', color='g', label='Buy', s=100)
    ax.scatter(merged_data.loc[sell_indices, 'DateTime'], merged_data.loc[sell_indices, 'Price'], marker='v', color='r', label='Sell', s=100)

    # Annotate the markers with quantity
    for i, row in merged_data.iterrows():
        if not pd.isna(row['Side']):
            ax.annotate(f"Price: {row['Price']}\nQty: {row['Quantity'] if 'Quantity' in row else 'N/A'}", (row['DateTime'], row['Price']), textcoords="offset points", xytext=(0, 10), ha='center')

    # Add labels, title, and legend
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title(f'{stock_name} Price and Buy/Sell Transactions')
    ax.legend()

    # Show the plot
    ax.grid()
    plt.tight_layout()
    
    plt.savefig(f"python_scripts/graphs/{stock_name}.png", format='png')

    plt.close()

plot_stock_data("NAM-INDIA")