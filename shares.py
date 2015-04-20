__author__ = 'petermarschel'


import requests
import bs4
import re

response = requests.get("http://finance.yahoo.com/ks?s=IBM")

soup = bs4.BeautifulSoup(response.text)

# Process the HTML to get prev close
shares_out = soup.find_all(name="td", text=re.compile("Shares Outstanding"))
target = shares_out[0]

print(target)