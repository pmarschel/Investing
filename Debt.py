__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

std = soup.find_all(name="td", text=re.compile("Long Term Debt"))
target = std[0]
sib = target.next_sibling
print(sib.string)


target = std[1]
sib = target.next_sibling
print(sib.string)
