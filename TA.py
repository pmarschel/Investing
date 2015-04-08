__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

tot_assets = soup.find_all(name="strong", text=re.compile("Total Assets"))

target = tot_assets[0]

p=re.compile('[0-9]*')

parent = target.parent.parent
for node in parent.contents:

    test = ''.join(node.contents[1])

    test2=p.findall(test)
