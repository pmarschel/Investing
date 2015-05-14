__author__ = 'pemarsc'

import requests
import bs4
import re

ticker = "BLUE"

URL_ROOT = "https://www.google.com/finance?q="
URL_TOT = URL_TOT = URL_ROOT + "NASDAQ" + "%3A" + ticker
response = requests.get(URL_TOT)
print(URL_TOT)
soup = bs4.BeautifulSoup(response.text)


target = soup.find_all(name="table", class_="snap-data")
#target = soup.find_all(name="td", text=re.compile('Mkt Cap'))
elements = list(target[1].children)
print(elements[9].contents)

#MC_group = elements[9].contents

#print(MC_group[3].contents[0])
#node = target.parent.contents

'''p=re.compile('[0-9]*')
result = p.findall(node[3].string)

print(result)
print(result[0]!='')

if result[0]!= '':
    print(int(result[0]))'''

