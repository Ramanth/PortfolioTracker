from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import clean_currency_text, get_symbol_by_name, insert_into_current_price, insert_price_change_if_difference, notify

# Set the remote debugging address for the Chrome browser
chrome_debugger_address = "localhost:9222"  # Replace with the correct address

# Create a ChromeOptions instance
chrome_options = webdriver.ChromeOptions()

# Add the remote debugging address to the options
chrome_options.add_experimental_option('debuggerAddress', chrome_debugger_address)

# Connect to the existing Chrome browser instance
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://groww.in/user/watchlist/stocks")  # For example, navigate to a webpage
while True:
    notify("Scripts", "analyzing")
    # Now you can use 'driver' to interact with the open Chrome browser
   
    time.sleep(5)
    price_snapshot = []

    xpath = "//div[contains(@class,'wlsl47CompanyNameLink')]"
    stocks = driver.find_elements(By.XPATH, xpath)
    for el in stocks:
        xpath_price = "//div[@title='" + el.text + "']/ancestor::div[1]/following-sibling::div[2]"
        price = driver.find_element(By.XPATH, xpath_price).text
        json_object = {
            "symbol": get_symbol_by_name(el.text),
            "price":clean_currency_text(price)
        }

        price_snapshot.append(json_object)

    insert_into_current_price(price_snapshot)
    insert_price_change_if_difference(price_snapshot)
    print("------------  end    ----------------------")

    time.sleep(60*10)

driver.close()

