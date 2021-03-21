#!/usr/bin/env python

# Import the required libraries
import pandas as pd  # Manipulating dataframe library
import requests  # Retrieves HTML from the BoE website
from bs4 import BeautifulSoup  # Library for parsing HTML
from dateutil.parser import parse  # Library manipulate date formats

# BoE url in README file
boe_url = "http://www.bankofengland.co.uk\
    /boeapps/iadb/fromshowcolumns.asp?\
        Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=ALL&VFD=N&\
            html.x=20&html.y=22&CSVF=TT&C=5JK&Filter=N"

# Requests the HTML code from BoE website with all SONIA rates
boe_page = requests.get(boe_url)
# Creates parse tree with HTML code
boe_html_tree = BeautifulSoup(boe_page.content, 'html.parser')
# Initiate empty list for storing website text
boe_text = []

for text in boe_html_tree.find_all('td'):
    # loop  over elements with 'td' tag in the HTML code
    # The td element has the text with dates and rates
    text_string = text.get_text().replace("\t", "")
    text_string = text_string.replace("\n", "")
    text_string = text_string.replace("\r", "")
    boe_text.append(text_string)

dates_and_rates_raw = boe_text[10:]  # first 10 elements are irrelevant

sonia_data = {"Date": list(), "SONIA": list()}

for text in dates_and_rates_raw:
    """Separates dates and rates from string list
    This for loop uses a try and except statement.

    By forcing evey iterable string to convert into a float we can identify
    wether the string contains a date or a rate if a ValueError is generated.

    date_or_rate data type is currently a string

    If float(date_or_rate) generates ValueError:
        String is not a SONIA rate, hence it must be a date
        Add to end of Date list
    Else:
        String did not generate ValueError, it must be a float
        Add to end of
    """
    try:
        sonia_data["SONIA"].append(float(text))
    except ValueError:
        text = parse(text).strftime('%d/%m/%Y')  # UK date format
        sonia_data["Date"].append(text)

num_spaces = 6
current_spaces = 0
while current_spaces < num_spaces:
    # The while loop below will add six additional blank cellls
    # on top of the excel table so the analyst can populate them
    # with the respective business dates and/or Alex's SONIA rate
    sonia_data['Date'].append(None)
    sonia_data['SONIA'].append(None)
    current_spaces += 1

# Create, sort, and store the csv table
sonia_dataframe = pd.DataFrame(sonia_data)
sonia_dataframe.index = sonia_dataframe['Date']
sonia_dataframe.drop('Date', axis=1, inplace=True)
sonia_dataframe = sonia_dataframe[::-1]  # Sort in descending order
sonia_dataframe.to_csv('SONIA.csv', sep=',')  # file is saved in current folder
