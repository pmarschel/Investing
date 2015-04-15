__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

std = soup.find_all(name="td", text=re.compile("Long Term Debt"))
target = std[0]

STD = []

p=re.compile('[0-9]*')

for i in range(4):
    target = target.next_sibling
    STD.append(''.join(p.findall(target.string)))

print(STD)
STD = [ '0' if x == '' else x for x in STD ]
print(STD)

results = [int(i) for i in STD]
print(results)

target = std[1]
sib = target.next_sibling
print(sib.string)
