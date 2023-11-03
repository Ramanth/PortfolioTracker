import json
import os
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
from plyer import notification
import pandas as pd
import datetime
from tinydb import TinyDB, Query

def get_stock_price(symbol):
    try:
        # Construct the search URL
        search_url = f"https://www.screener.in/company/{symbol}/consolidated/"
        # Send a GET request to the search URL
        response = requests.get(search_url)
        # Create a BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')
        lxml_tree = etree.HTML(str(soup))
        xpath_expression = "//*[normalize-space(text()) = 'High / Low']/following-sibling::span/span"
        elements = lxml_tree.xpath(xpath_expression)
        high = elements[0].text or "NA"
        low = elements[1].text or "NA"
        xpath_current = "//*[normalize-space(text()) = 'Current Price']/following-sibling::span/span"
        elements = lxml_tree.xpath(xpath_current)
        current = elements[0].text or "NA"
        current = current.replace(",","")
        return float(current)
    except Exception as exp:
        print("getting from google "+ symbol)
        time.sleep(2)
        return get_stock_price_google(symbol)


def get_stock_price_google(symbol):
    try:
        # Prepare the search query
        query = f"{symbol} stock price"
        url = f"https://www.google.com/search?q={query}"

        # Send a GET request to Google and retrieve the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors in the request

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element containing the stock price
        price_element = soup.find('div', class_='BNeawe iBp4i AP7Wnd')

        # Extract the price value
        if price_element:
            x =  price_element.text
            price = float(x.split(" ")[0].replace(",", ""))
            return price
        else:
            return "Price not found"
    except:
        print("google threw exception")
    

mappings = {"CREDGRAMEEN":"CREDITACC","IOCL":"IOC", "INFOEDGE":"NAUKRI", "INFOSYS":"INFY", "ENGENEERIND":"ENGINERSIN", "AIRTEL":"BHARTIARTL", "BIRLASOFT":"BSOFT", "LIC":"LICI", "VEDANTA":"VEDL", "SONATA":"SONATSOFTW"}


symbols = [
    "SANSERA",
    "SAIL",
    "SONATA",
    "SUPRAJIT",
    "HAPPSTMNDS",
    "HINDALCO",
    "IOCL",
    "WIPRO",
    "TATACHEM",
    "ICICIBANK",
    "CREDGRAMEEN",
    "NAM-IND",
    "ZOMATO",
    "CMSINFO",
    "INFOEDGE",
    "SUZLON",
    "JUBLFOOD",
    "IIFLSEC",
    "TRIDENT",
    "TATAMOTORS",
    "LIC",
    "ITC",
    "MOTHERSON",
    "INFOSYS",
    "AIRTEL",
    "JSWSTEEL",
    "KIRLOSENG",
    "ENGENEERIND",
    "BHEL",
    "BIRLASOFT",
    "HDFCBANK",
    "PPLPHARMA",
    "VEDANTA",
    "AARTIDRUGS",
    "MEDPLUS",
    "RAILTEL",
    "GMBREW",
    "NMDC",
    "TATASTEEL",
    "JSWENERGY",
    "POWERGRID",
    "VRLLOG",
    "KPITTECH",
    "GPIL",
    "HINDCOPPER",
    "HDFCLIFE",
    "ASHOKLEY",
    "SBICARD",
    "SUNPHARMA",
    "ATULAUTO",
    "SULA",
    "SANGHIIND",
    "FINPIPE",
    "LATENTVIEW",
    "APLAPOLLO",
    "MOTILALOFS",
    "FIVESTAR",
    "CIEINDIA",
    "AARTIIND",
    "EMAMILTD"
  ]

prices = {}

for symbol in symbols:
    origsymbol = symbol
    if symbol in mappings.keys():
        symbol = mappings[symbol]
    
    price = get_stock_price(symbol)
    print(symbol, " ", price)
    prices[origsymbol]=price


with open("prices.json", "w") as json_file:
    json.dump(prices, json_file)
