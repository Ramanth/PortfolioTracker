import pandas as pd
import json

# Replace 'your_excel_file.xlsx' with the path to your Excel file
excel_file_path = 'data.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path)

# Initialize an empty dictionary to store the data
stock_data = {}

# Iterate through each row in the DataFrame and add "Name" and "Price" to the dictionary
for index, row in df.iterrows():
    stock_name = row['Name']
    stock_price = row['Price']
    stock_data[stock_name] = stock_price

# Write the dictionary to a JSON file named 'prices.json'
with open('prices.json', 'w') as json_file:
    json.dump(stock_data, json_file, indent=4)

