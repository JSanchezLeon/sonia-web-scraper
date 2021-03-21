#!/usr/bin/env python

""" The following script scrapes the BoE website and parses all available SONIA rates into excel"""
#Import the required libraries
import pandas as pd #Pandas for manipulating dataframe and creating excel table
import requests #Retrieves HTML from the BoE website
from bs4 import BeautifulSoup #Library that simplyfies the parsing process and extracting the rights info from the HTML code
from dateutil.parser import parse #Library to help convert date formats

#DONT TOUCH URL "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=ALL&VFD=N&html.x=20&html.y=22&CSVF=TT&C=5JK&Filter=N"

boe_url = "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=ALL&VFD=N&html.x=20&html.y=22&CSVF=TT&C=5JK&Filter=N"

#Requests the HTML code from BoE website with all SONIA rates, it returns the website HTML in JSON notation
boe_page = requests.get(boe_url)

#Creates parse tree with HTML code
boe_html_tree = BeautifulSoup(boe_page.content, 'html.parser')

#Initiate empty list to store text
boe_text = []
#This for loop iterates over all the objects with a 'td' tag in the HTML code.
for text in boe_html_tree.find_all('td'):
    text_string = text.get_text().replace("\t","")
    text_string = text_string.replace("\n","")
    text_string = text_string.replace("\r","")
    boe_text.append(text_string)

body = boe_text[10:]

sonia_data = {"Date": [],
             "SONIA": []}
for i in body:
    try:
        sonia_data["SONIA"].append(float(i))
    except ValueError:
        i = parse(i).strftime('%d/%m/%Y')
        sonia_data["Date"].append(i)

#print("the last date with SONIA is {}".format(sonia_data["Date"][-1]))

num_spaces = 6
current_spaces = 0
while current_spaces < num_spaces:
    sonia_data['Date'].append(None)
    sonia_data['SONIA'].append(None)    
    current_spaces += 1


df = pd.DataFrame(sonia_data)

df.index = df['Date']

df.drop('Date',axis = 1,inplace = True)

df = df[::-1]

df.to_csv('SONIA.csv', sep=',')