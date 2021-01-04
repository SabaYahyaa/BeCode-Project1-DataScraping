
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup  #BeautifulSoup is a Python library
                                    #for pulling data out of HTML and XML files.
import csv
import urllib.request
import urllib.parse
import urllib.error
import ssl
import re
import pandas as pd
import np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import seaborn as sns
import pdb
import requests

with open('myurllist-2.csv', 'r') as f:
    urls = next(csv.reader(f))
    #urls = list(csv.reader(f))





#Note: when we have a list of urls, Beautifulsoup gives an error to overcome this problem,
# we have either use get_headers or urllib.request (this is not working), so I need to try with urllib3 later
def get_headers():
    #Headers
    headers={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language':'en-US,en;q=0.9',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

    return headers

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


locality=[] #ok
typeofproperty=[] #ok
price=[] #ok
NumberBedRooms=[]  #ok, bedrooms
NumberBathrooms=[] #ok,
kitchenfullyequipped=[]
HabitableArea=[]
furnished=[]
openfire=[]
Surface_area_of_the_plot_of_land=[]
swimming_pool=[]
state_of_the_building=[]
Open_fire=[] #(Yes / No)
Terrace=[]#(Yes / No) If yes: Area
Area_of_Terrace=[]
Garden=[]#(Yes/No)
Area_of_Garden=[]#If yes: Area
Surface_of_Land=[]
Surface_area_of_PlotLand=[]
Number_of_facades=[]
Swimming_pool=[]#(Yes / No)
State_of_Building=[]  #(New, to be renovated, ...)
HeatingType=[] #ok
ElectricalInspectionReport=[] #ok Electrical inspection report

# for url in urls: #extract from te csv file
# count=1 # for pagination





#soup = BS(htmltext,'html.parser')

print("------------------------------")
print("------------------------------")
print("------------------------------")
print("------------------------------")

# print(urls[0])
# print(urls[1])
# pdb.set_trace()


############"
#####  TO DO....................
#############
#ask christope for correct links, I will scap
urls=urls[0:15]
#urls=urls[8:10]

# "https://www.trulia.com/for_rent/Oakland,CA/1p_beds/SINGLE-FAMILY_HOME_type
# url="https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE"


for url in urls:
    print(url)
    # Note: I will scrap first from only the first page, to be sure about the result
    req = Request(url, headers=get_headers())  # req all headers
    htmlfile = urlopen(req)
    htmltext = htmlfile.read()


    r = requests.get(url)
    print(url, r.status_code)
    soup = BeautifulSoup(r.content,'html.parser')

    #extract locality
    container = soup.find_all('div', attrs={"class":"property__container"})
    for c in container:  #price, locality, from Dilara
            for link in c.findAll('h1', attrs={'class':"address"}):
             # print(link.text)
              locality.append(link.text.strip())
    # extract price
    for c in container:  #price, locality, type of property from Dilara
            for link in c.findAll("span", attrs={"itemprop":"price"}):
             # print(link.text)
              price.append(link.text)

   # extract type_of_property
    for c in container:  # price, locality, type of property from Dilara
        for link in c.findAll("div", attrs={"class": "type"}):
            typeofproperty.append(link.text.partition(' ')[0].strip()) #get the first word only
            Type_checking=link.text.partition(' ')[0].strip() #the table of html file is different depending on
                                           # the type of property (flat or house), so check if you have flat or house

    print(Type_checking)

    # 444444444444444444444444444444444444444
    table = soup.find_all("table")
    #print(table[1])
    #to iterate for all tables
    # for each_table in table:
    #     print(each_table.find("tbody"))
    #     print("----------------------------")



    if (Type_checking == "House" or Type_checking == "Land"):
        # I want only table[1] to scrap features of houses
        rows=table[1]
        # a=[]
        # for item in rows.find_all("tr"):
        #     for sub_item in item.find_all("td"):
        #          a.append(sub_item.text.strip().replace(',',''))
        # print(table)

        # pdb.set_trace()

        # 5555555555555555555555555
        # 5555555555555555555555555
        # 5555555555555555555555555

        # <table>
        #     < tbody >
        #     < tr >
        #         < td >
        #             < td > #I could not scrap here?????????????????????????????, the value of area for example
        # 5555555555555555555555555
        # 5555555555555555555555555
        # 5555555555555555555555555


        results = {}
        for item in rows.find_all("tr"):
            aux = item.findAll('td')
            results[aux[0].string] = aux[1].string

        # print (results)
        #
        # pdb.set_trace()
        # for k, v in results.items():
        #     print(k, v)

        #bed rooms
        if 'Bedrooms' in results: #we have land for sale, so there is no bedroom key
            NumberBedRooms.append(results['Bedrooms'])
        else:
            NumberBedRooms.append(0)

        #Habitable area
        if 'Bathrooms' in results: #we have land for sale, so there is no bedroom key
            NumberBathrooms.append(results['Bathrooms'])
        else:
            NumberBathrooms.append(0)

        #Heating type
        if 'Heating type' in results: #we have land for sale, so there is no bedroom key
            HeatingType.append(results['Heating type'].strip())
        else:
            HeatingType.append('None')

        #Electrical inspection report
        if 'Electrical inspection report' in results:  # we have land for sale, so there is no bedroom key
            ElectricalInspectionReport.append(results['Electrical inspection report'].strip())
        else:
            ElectricalInspectionReport.append('None')

    # end here 7777777777777777777777777777777777777777777
# end here 7777777777777777777777777777777777777777777

    elif (Type_checking == "Flat"):
        # 55555555555555555555555555555555
        # 55555555555555555555555555555555
        # I want only table[0] to scrap features of flats
        rows=table[0]
        results = {}
        for item in rows.find_all("tr"):
            aux = item.findAll('td')
            results[aux[0].string] = aux[1].string

        if 'Bedrooms' in results: #we have land for sale, so there is no bedroom key
            NumberBedRooms.append(results['Bedrooms'])
        else:
            NumberBedRooms.append(0)

            # area
            # Habitable area
        if 'Bathrooms' in results:  # we have land for sale, so there is no bedroom key
                NumberBathrooms.append(results['Bathrooms'])
        else:
                NumberBathrooms.append(0)

        # Heating type
        if 'Heating type' in results:  # we have land for sale, so there is no bedroom key
            HeatingType.append(results['Heating type'].strip())
        else:
            HeatingType.append(0)

        # Electrical inspection report
        if 'Electrical inspection report' in results:  # we have land for sale, so there is no bedroom key
            ElectricalInspectionReport.append(results['Electrical inspection report'].strip())
        else:
            ElectricalInspectionReport.append('None')

        # 55555555555555555555555555555555
        # 55555555555555555555555555555555
    else:
        pass
    # 444444444444444444444444444444444444444
#{ 'Bathrooms': '1',
# 'Habitable area': None,
# 'Facade width': '9,3m',
# 'Lot size': None,
# '\n\t\t\t\t\tBackside/Garden orientation\n\t\t\t\t': '\n\t\t\t\t\tWest\n\t\t\t\t',
# 'Year built': '1972',
# 'Year renovated': '2015',
# 'Building placement': '\n\t\t\t\tTerraced\n\t\t\t',
# 'Heating type': '\n\t\t\t\t\tGas\n\t\t\t\t',
# 'Garages': '1',
# 'Cadastral income': '€ 430',
# 'Electrical inspection report': '\n\t\t\t\t\tAvailable, conform\n\t\t\t\t',
# 'Planning permit': '\n\t\t\t\t\tYes\n\t\t\t\t',
# 'Subdivision permit': '\n\t\t\t\t\tNo\n\t\t\t\t',
# 'Summons issued': '\n\t\t\t\t\tNo\n\t\t\t\t',
# 'Pre-emption': '\n\t\t\t\t\tYes\n\t\t\t\t',
# 'Flood-prone area': '\n\t\t\t\t\tNot in flood-prone area\n\t\t\t\t'}

print("------------------------------------")
print(locality)
print(typeofproperty)
print(price)
print(NumberBedRooms)
print(NumberBathrooms)
print(HeatingType)
print(ElectricalInspectionReport)

#create a data frame
dic={'locality':locality,
     'typeofproperty':typeofproperty,
     'price':price,
     'NumberBedRooms':NumberBedRooms,
     'NumberBathrooms':NumberBathrooms,
     'HeatingType':HeatingType,
     'ElectricalInspectionReport':ElectricalInspectionReport }

df=pd.DataFrame(dic)
#print(df.head())
df.to_csv('RealStateData.csv', encoding='utf-8', index=False)



price = []
typeofproperty = []
locality = []
bedrooms = []
bathrooms=[]
area=[]
n_pages=0

#create a data frame
dic={'price':price,
     'typeofproperty':typeofproperty,
     'locality':locality,
     'bedrooms':bedrooms,
     'bathrooms':bathrooms,
     'area':area }

df=pd.DataFrame(dic)
#print(df.head())
df.to_csv('RealStateData.csv', encoding='utf-8', index=False)

types = [n.strip() for n in type] use:

for n in type:
    if n.strip != None:
        types.append(n.strip)
    else:
        types.append('None')