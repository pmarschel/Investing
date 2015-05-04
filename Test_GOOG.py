__author__ = 'pemarsc'

import requests
import bs4
import re
import datetime

ticker = "BIIB"

# Get the balance sheet
URL_ROOT = "https://www.google.com/finance?fstype=ii&q="

URL_TOT = URL_ROOT + ticker
print(URL_TOT)

response = requests.get(URL_TOT)
soup = bs4.BeautifulSoup(response.text)

itemName = "Total Assets"
rank=1

target = soup.find_all(name="td", text=re.compile(itemName))[rank]

results = []

for node in target.next_siblings:
    s = node.string
    if s != '\n':
        s = s.replace(',', '')
        results.append(float(s))


print(results)