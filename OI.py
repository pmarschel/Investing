# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 09:55:16 2015

@author: pemarsc
"""

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/is?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

# Process the HTML to get OI
tot_assets = soup.find_all(name="strong", text=re.compile("Operating Income or Loss"))
target = tot_assets[0]
parent = target.parent.parent

p=re.compile('[0-9]*')
temp = []

for node in parent.contents:
    # raw contents
    raw_contents = ''.join(node.contents[1])
    
    # get numbers separated by ,
    nums=p.findall(raw_contents)
    
    # stick the nums together to get one big num
    assets = ''.join(nums)

    # put them in the list
    temp.append(assets)

# turn list to int and assign to member variable
results = [int(i) for i in temp[1:]]
print(results)