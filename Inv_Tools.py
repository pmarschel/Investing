__author__ = 'petermarschel'

import requests
import bs4
import re

class Company:

    def __init__(self, ticker):

        self.ticker = ticker
        self.updated = "some date"

        self.debt = 0
        self.assets = 123

        self.price = 52.3
        self.shares = 100

    def getTicker(self):
        return self.ticker

    def getUpdated(self):
        return self.updated

    def getDebt(self):
        return self.debt

    def getAssets(self):
        return self.assets

    def getPrice(self):
        return self.price

    def getShares(self):
        return self.shares

    def initDebt(self):

        response = requests.get("http://finance.yahoo.com/q/bs?s=AAPL")
        soup = bs4.BeautifulSoup(response.text)

        tot_assets = soup.find_all(name="strong", text=re.compile("Total Assets"))
        target = tot_assets[0]

        parent = target.parent
        aunt = parent.next_sibling
        cousin = aunt.contents[1]
        self.debt = int(cousin.string)
