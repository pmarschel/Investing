__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/is?s=AAPL&annual")

soup = bs4.BeautifulSoup(response.text)

std = soup.find_all(name="td", text=re.compile("Research Development"))
target = std[0]

sibs = target.next_siblings

for sib in sibs:
    print(sib.string)
