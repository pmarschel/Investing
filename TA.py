__author__ = 'pemarsc'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")

soup = bs4.BeautifulSoup(response.text)

tables = soup.find_all('table')
table_ind= tables[1]
print(len(tables))

count = 0

for table in soup.find_all('table'):

    row_count = 1
    for row in table.find_all('tr'):
        row_count += 1

    print(str(count) + ' ' + str(row_count))
    count += 1

tot_assets = soup.find_all(name="strong", text=re.compile("Total Assets"))
target = tot_assets[0]

parent = target.parent
aunt = parent.next_sibling
cousin = aunt.contents[1]
print(cousin.string)
