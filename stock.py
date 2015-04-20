__author__ = 'petermarschel'

import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/q?s=IBM")

soup = bs4.BeautifulSoup(response.text)

# Process the HTML to get prev close
prev_close = soup.find_all(name="th", text=re.compile("Market Cap:"))
target = prev_close[0]

raw=target.next_sibling.string

raw_mc = float(raw[0:-1])
raw_mult = raw[-1]

if raw_mult=='B':
    mult = 1000000
else:
    mult = 1000

print(raw_mc)
print(mult)
print(raw_mc * mult)