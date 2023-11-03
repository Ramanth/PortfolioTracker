from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from utils import clean_currency_text, convert_date_to_iso, get_symbol_by_name, insert_into_transactions, add_time_to_date, insert_log_in_order


def filter_objects_by_current_date(arr, filterDate = ""):
    current_date_str = convert_date_to_iso(datetime.date.today().isoformat(), '%Y-%m-%d',output_format="%Y-%m-%d")
    if filterDate != "":
        current_date_str = convert_date_to_iso(filterDate, '%Y-%m-%d', output_format="%Y-%m-%d")
    filtered_objects = [obj for obj in arr if obj.get("date").startswith(current_date_str)]
    return filtered_objects


def insert_into_log_file(filtered_transactions):
    for transaction in filtered_transactions:
        insert_log_in_order(transaction['date'], str(transaction['symbol']) + " - " + str(transaction['side']) + " " + str(transaction['quantity']) + " @ " + str(transaction['price']))


# Set the remote debugging address for the Chrome browser
chrome_debugger_address = "localhost:9222"  # Replace with the correct address
# Create a ChromeOptions instance
chrome_options = webdriver.ChromeOptions()
# Add the remote debugging address to the options
chrome_options.add_experimental_option('debuggerAddress', chrome_debugger_address)
# Connect to the existing Chrome browser instance
driver = webdriver.Chrome(options=chrome_options)
# Now you can use 'driver' to interact with the open Chrome browser
driver.get("https://groww.in/user/order/stocks")  # For example, navigate to a webpage
time.sleep(5)
time.sleep(5)
transaction_date = ""
transactions_data = []

xpath = "//div[@class='stocksOrders_stk101MainBox__NOFFY']//a"
transactions = driver.find_elements(By.XPATH, xpath)

for transaction in transactions:
    date_text = transaction.find_element(By.XPATH, "preceding-sibling::div").text.split(", ")[-1]
    if date_text:
        transaction_date = date_text

    transaction_info = transaction.text.split("\n")
    print(transaction_info)
    date_value = convert_date_to_iso(transaction_date)
    date_time = add_time_to_date(date_value, transaction_info[-1])
    obj = {
        "date": date_time,
        "symbol": get_symbol_by_name(transaction_info[0]),
        "side": transaction_info[1],
        "quantity": clean_currency_text(transaction_info[4]),
        "price": clean_currency_text(transaction_info[6])
    }
    # print(transaction_info[0])
    transactions_data.append(obj)

filtered_transactions = filter_objects_by_current_date(transactions_data , "2023-11-02")
insert_into_transactions(filtered_transactions)
insert_into_log_file(filtered_transactions)
time.sleep(500)
driver.close()

