__author__ = 'pemarsc'

import requests
import bs4
import re
import datetime

response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

std = soup.find_all(name="td", text=re.compile("Period Ending"))
target = std[0]

STD = []

for i in range(4):
    target = target.next_sibling
    STD.append(datetime.datetime.strptime(target.string, '%b %d, %Y').date())

print(STD)
