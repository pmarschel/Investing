__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/is?s=AAPL&annual")

soup = bs4.BeautifulSoup(response.text)

std = soup.find_all(name="td", text=re.compile("Research Development"))
target = std[0]

sibs = target.next_siblings

p=re.compile('[0-9]*')
result = []

for sib in sibs:
    result.append(''.join(p.findall(sib.string)))

result = [ '0' if x == '' else x for x in result ]
result = [int(i) for i in result]

print(result)