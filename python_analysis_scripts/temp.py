import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("my_database.db")
query = "SELECT * FROM current_price"
current_price_df = pd.read_sql_query(query, conn)

print(current_price_df)