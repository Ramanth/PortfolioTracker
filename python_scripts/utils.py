from datetime import datetime
import sqlite3
from plyer import notification
from plotting_utils import plot_stock_data

from speech_utils import speak_drop_alert

# conn = sqlite3.connect("my_database.db")
# cursor = conn.cursor()
# cursor.execute("DELETE FROM super_portfolio WHERE Stock = 'LATENTVIEW'")
# conn.commit()
# conn.close()

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

def print_last_five_transactions(stock_name):
    connection = sqlite3.connect('my_database.db')  # Replace 'your_database.db' with your actual database file name
    cursor = connection.cursor()
    
    # Use a SELECT statement to fetch the last five transactions for the specified Stock name
    cursor.execute('''
    SELECT SNo, Stock, Side, Price, Quantity, Datetime
    FROM transactions
    WHERE Stock = ?
    ORDER BY Datetime DESC
    LIMIT 5
    ''', (stock_name,))
    
    transactions = cursor.fetchall()
    
    if transactions:
        print(f"    Transactions")
        for transaction in transactions:
            print(f"        [{transaction[5]}] {transaction[1]}  {transaction[2]} {transaction[4]} @ {transaction[3]}")
    else:
        print(f"    No transactions found for {stock_name}.")
    
    connection.close()

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=1  # Duration to display the notification (in seconds)
    )

def log(title, message):
    # Open the file in append mode
    with open('logfile.log', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Append content to the file
        file.write(f'[{timestamp}] : {title}  -  {message}')
        file.write('\n')

def insert_log_in_order(new_datetime_str, new_string):
    filename = "logfile.log"
    new_datetime = datetime.strptime(new_datetime_str, '%Y-%m-%d %H:%M:%S')

    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())

    new_line = f"[{new_datetime.strftime('%Y-%m-%d %H:%M:%S')}] : {new_string}"

    for i, line in enumerate(lines):
        if line.startswith('['):
            timestamp_str = line.split(']')[0][1:]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            if new_datetime < timestamp:
                lines.insert(i, new_line)
                break
    else:
        lines.append(new_line)

    with open(filename, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def insert_price_change_if_difference(data, threshold=1.5):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        for item in data:
            new_price =  item['price']
            symbol = item['symbol']

            # Get the last inserted price for the given symbol
            cursor.execute("SELECT Price FROM price_changes_10_23 WHERE Stock = ? ORDER BY DateTime DESC LIMIT 1", (symbol,))
            last_price = cursor.fetchone()

            if last_price:
                last_price = last_price[0]

                # Calculate the percentage difference
                percent_difference = abs((new_price - last_price) / last_price) * 100

                # Insert the new price if the percentage difference is greater than the threshold
                if percent_difference > threshold:
                    cursor.execute("INSERT INTO price_changes_10_23 (Stock, Price, DateTime) VALUES (?, ?, datetime('now'))", (symbol, new_price))
                    conn.commit()
                    diff = (new_price - last_price)
                    neg_symbol =  "-" if diff < 0  else "+"
                    print(f"{symbol}")
                    print(f"    {new_price}, Diff:{diff:.2f}, Percent Difference:                     {neg_symbol}{percent_difference:.2f}%")
                    print_last_five_transactions(symbol)
                    speak_drop_alert(symbol, new_price,  f"{neg_symbol}{percent_difference:.2f}%")
                    plot_stock_data(symbol)
                    #notify(symbol, f"Diff:{diff:.2f}, Percent Difference: {neg_symbol}{percent_difference:.2f}%")
                    log(symbol, f" {new_price} - Diff:{diff:.2f}, Percent Difference: {neg_symbol}{percent_difference:.2f}%")
                # else:
                #     print(f"Price change for {symbol} is within {threshold:.2f}%, skipping.")
            else:
                # Insert the first record for the symbol
                cursor.execute("INSERT INTO price_changes_10_23 (Stock, Price, DateTime) VALUES (?, ?, datetime('now'))", (symbol, new_price))
                conn.commit()
                print(f"First entry for {symbol}: {new_price}")

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()

def insert_into_current_price(data):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM current_price")
        # Iterate through the data and insert each item into the "current_price" table
        for item in data:
            cursor.execute("INSERT INTO current_price (stock, price) VALUES (?, ?)", (item['symbol'], item['price']))

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the database connection
        conn.close()

def insert_into_transactions(data):
    # Connect to the SQLite database
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    # Iterate through the list of dictionaries and insert each item into the table
    for item in data:
        cursor.execute('''
            INSERT INTO transactions (Stock, Side, Price, Quantity, Datetime)
            VALUES (?, ?, ?, ?, ?)
        ''', (item['symbol'], item['side'], item['price'], item['quantity'], item['date']))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def clean_currency_text(text):
    # Remove rupee symbol and commas
    cleaned_text = text.replace('₹', '').replace(',', '')
    return float(cleaned_text)

def get_symbol_by_name(stock_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        # Define the SQL query to retrieve the Symbol for the given stock_name
        query = "SELECT Symbol FROM mappings WHERE Name = ?"
        # Execute the query with the stock_name parameter
        cursor.execute(query, (stock_name,))
        # Fetch the result
        result = cursor.fetchone()
        if result:
            symbol = result[0]
            return symbol
        else:
            return None
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None
    finally:
        # Close the database connection
        conn.close()

def convert_date_to_iso(date_string, format="%d %b %Y", output_format="%Y-%m-%d %H:%M:%S"):
    # Define the format of the input date
    input_format = format
    # Parse the input date string into a datetime object
    date_object = datetime.strptime(date_string, input_format)
    # Convert the datetime object to a string in SQLite DATETIME format
    sqlite_datetime = date_object.strftime(output_format)
    return sqlite_datetime

def add_time_to_date(date_string, time_value):
    # Parse the date string and extract the date part
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    # Parse the time value and extract the time part
    time = datetime.strptime(time_value, "%I:%M %p").time()

    # Combine the date and time to get the complete date-time
    complete_datetime = datetime.combine(date.date(), time)

    return complete_datetime.strftime("%Y-%m-%d %H:%M:%S")
