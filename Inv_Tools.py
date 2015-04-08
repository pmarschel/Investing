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

        self.initBS()

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

    def initBS(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/bs?s="
        response = requests.get(URL_ROOT + self.getTicker())
        soup = bs4.BeautifulSoup(response.text)

        self.processAssets(soup)
        self.processDebt(soup)


    def processAssets(self, soup):

        # Process the HTML to get total assets
        tot_assets = soup.find_all(name="strong", text=re.compile("Total Assets"))
        target = tot_assets[0]

        parent = target.parent
        aunt = parent.next_sibling
        cousin = aunt.contents[1]

        p=re.compile('[0-9]*')
        self.assets = int(''.join(p.findall(cousin.string)))

    def processDebt(self, soup):

        # Process the HTML to get STD and LTD
        tot_debt = soup.find_all(name="td", text=re.compile("Long Term Debt"))
        target = tot_debt[0]
        sib = target.next_sibling

        p=re.compile('[0-9]*')
        self.debt = int(''.join(p.findall(sib.string)))

        target = tot_debt[1]
        sib = target.next_sibling
        self.debt = self.debt + int(''.join(p.findall(sib.string)))
