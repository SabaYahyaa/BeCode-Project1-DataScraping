# All our packages required for the project
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen, Request
from requests import get
import requests
import pdb
import re
import pandas as pd

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# Variables

price = []
type_of_property = []
locality= []
bed_rooms = []
bath_rooms = []
area = []
n_pages = 0

# This is our loop to go through all the pages of the website
for page in range(0, 2):
    n_pages += 1
    url = 'https://www.realo.be/en/search/for-sale?page=' + str(page)
    req = get(url, headers=headers)


    html_soup = BeautifulSoup(req.text, 'html.parser')

    house_containers = html_soup.find_all('li')
    #####################################################
    #  "Price" list
    ####################################################
    for p in html_soup.find_all('div', attrs={"data-type": "label"}):
        price.append(re.findall(r'\d+', p.text)[0])
        #print(re.findall(r'\d+', p.text)[0])
        #pdb.set_trace()

    #####################################################
    #  "Locality list
    ####################################################
    for l in html_soup.find_all('div', attrs={"class": "address truncate"}):
        if l.text.strip()!=None:
            locality.append(l.text.strip())
        else:
            locality.append('None')

    #####################################################
    #  Type of property list
    ####################################################
    for t in html_soup.find_all('div', attrs={'class': 'ways-types truncate'}):
        if t.text.strip()!=None:
            type_of_property +=[t.text.partition(' ')[0].strip()]
        else:
            type_of_property += ['None']


    for c in html_soup.find_all('div', attrs={"class":"details truncate"}):
        lst=[]
        for stat in c.find_all('span'):
            lst.append(stat['class'])
        #     print((stat['class']))
        #     print(lst)

        #####################################################
        #  Bed rooms list
        ####################################################
        if ['icon', 'icn-dot', 'beds'] in lst: #we have room
            x=html_soup.find('span', attrs={"class": "icon icn-dot beds"})
            bed_rooms.append(x.text)
        else:
            bed_rooms.append(0)

        #####################################################
        #  Bath rooms list
        ####################################################
        if ['icon', 'icn-dot', 'baths'] in lst:  # we have room
            x = html_soup.find('span', attrs={"class": "icon icn-dot baths"})
            bath_rooms.append(x.text)
        else:
            bath_rooms.append(0)
        #####################################################
        #  area list
        ####################################################
        if ['icon', 'icn-dot', 'area'] in lst:  # we have room
            x = html_soup.find('span', attrs={"class": "icon icn-dot area"})
            area.append(x.text)
        else:
            area.append(0)


print(len(locality))
print(len(price))
print(len(type_of_property))
print(len(bed_rooms))
print(len(bath_rooms))
print(len(area))

#create a data frame
dic={'Price':price,
     'Property_type':type_of_property,
     'locality':locality,
     'Bed_rooms':bed_rooms,
     'Bath_rooms':bath_rooms,
     'Area':area }

df=pd.DataFrame(dic)
#print(df.head(2))
#pdb.set_trace()
df.to_csv('RealStateData.csv', encoding='utf-8', index=False)