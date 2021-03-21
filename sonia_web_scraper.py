#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

from dateutil.parser import parse

all_data = input("Do you want all available dates? enter yes or no:\n")

if all_data == "yes":
    #DONT TOUCH "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=ALL&VFD=N&html.x=20&html.y=22&CSVF=TT&C=5JK&Filter=N"

    url = "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=ALL&VFD=N&html.x=20&html.y=22&CSVF=TT&C=5JK&Filter=N"
    year = input("Please enter the relevant year\n")
    month = input("Please enter the relevant month(e.g. March = 03)\n")
    

else:
    from_date = input("Please enter the start date strictly in the format 'day Mon year' e.g 1 Jan 2021\n" )
    to_date = input("Please enter the end date strictly in the format 'day Mon year' e.g 1 Jan 2021\n")
    from_date = from_date.split(" ")
    to_date = to_date.split(" ")

    FD, FM, FY = from_date[0], from_date[1], from_date[2]
    TD, TM, TY = to_date[0], to_date[1], to_date[2]
    #DONT_TOUCH "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD=1&FM=Jan&FY=2010&TD=17&TM=Mar&TY=2021&VFD=Y&html.x=19&html.y=14&CSVF=TT&C=5JK&Filter=N"
    #print("http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD={FD}&FM={FM}&FY={FY}&TD={TD}&TM={TM}&TY={TY}&VFD=Y&html.x=19&html.y=14&CSVF=TT&C=5JK&Filter=N".format(FD=FD,FM=FM,FY=FY,TD=TD,TM=TM,TY=TY))
    url = "http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?Travel=NIxIRxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD={FD}&FM={FM}&FY={FY}&TD={TD}&TM={TM}&TY={TY}&VFD=Y&html.x=19&html.y=14&CSVF=TT&C=5JK&Filter=N".format(FD=FD,FM=FM,FY=FY,TD=TD,TM=TM,TY=TY)
    
    month_dictionary = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,
    "May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,
    "Dec":12}
    for keys,values in month_dictionary.items():
        month_dictionary[keys] = str(values)
    year = TY
    month = month_dictionary[TM]

next_five_bd = input("======================================================\
    \nPlease enter the next 6 relevant business days up to the ipd separated by a coma\n")


page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

boe_text = []
for text in soup.find_all('td'):
    text_string = text.get_text().replace("\t","")
    text_string = text_string.replace("\n","")
    text_string = text_string.replace("\r","")
    boe_text.append(text_string)

body = boe_text[10:]

sonia_data = {"Date": [],
             "SONIA": []}
for i in body:
    try:
        sonia_data["SONIA"].append(round(float(i)/100, 6))
    except ValueError:
        i = parse(i).strftime('%m/%d/%Y')
        sonia_data["Date"].append(i)

#print("the last date with SONIA is {}".format(sonia_data["Date"][-1]))


next_five_bd = next_five_bd.split(",")
next_five_dates = [month + "/" + day + "/" + year for day in next_five_bd]

for date in next_five_dates:
    sonia_data['Date'].append(date)
    sonia_data['SONIA'].append(None)    


df = pd.DataFrame(sonia_data)

df.index = df['Date']

df.drop('Date',axis = 1,inplace = True)

df = df[::-1]

df.to_csv('SONIA.csv', sep=',')