__author__ = 'pemarsc'

import requests
import bs4
import re

ticker = "BLUE"

URL_ROOT = "https://www.google.com/finance?q="
URL_TOT = URL_ROOT + ticker
response = requests.get(URL_TOT)
soup = bs4.BeautifulSoup(response.text)
print(soup)

#target = soup.find_all(name="table", class_="snap-data")
target = soup.find_all(name="td", class_="key")
print(target)


#node = target.parent.contents

'''p=re.compile('[0-9]*')
result = p.findall(node[3].string)

print(result)
print(result[0]!='')

if result[0]!= '':
    print(int(result[0]))'''

