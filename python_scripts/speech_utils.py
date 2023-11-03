import pyttsx3
import sqlite3
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_name_by_symbol(stock_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        # Define the SQL query to retrieve the Symbol for the given stock_name
        query = "SELECT Name FROM mappings WHERE Symbol = ?"
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

def is_super_portfolio_stock(symbol):
    connection = sqlite3.connect('my_database.db')  # Replace 'portfolio.db' with your database file name
    cursor = connection.cursor()
    
    # Use a SELECT statement to check if the stock exists in the table
    cursor.execute('SELECT Stock FROM super_portfolio WHERE Stock = ?', (symbol,))
    
    result = cursor.fetchone()
    
    connection.close()
    
    return result is not None


def speak_drop_alert(symbol, curr_price, percent):
    name = get_name_by_symbol(symbol)
    is_superportfolio = is_super_portfolio_stock(symbol)
    is_super_text = "Attention! super portfolio stock " if is_superportfolio else ""
    text = f"Drop Alert, {is_super_text} {name} current price is {curr_price}, got changed by {percent}"
    speak(text)
