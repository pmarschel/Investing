__author__ = 'petermarschel'

import requests
import bs4
import re

class Company:

    def __init__(self, ticker):

        self.ticker = ticker.strip()

        if len(self.ticker) == 4:
            self.exchange = "NASDAQ"
        else:
            self.exchange = "NYSE"

        # Balance sheet quantities
        self.debt = []
        self.assets = []
        self.cash = []

        # P&L quantities
        self.OI = []
        self.AnnualRD = []

        # market related
        self.MarketCap = 0

        # error
        self.error = None
        self.OK = True
        self.dataValid = True

        try:
            soup = self.getParsedHTML()
            self.initBS(soup)
            self.initPL(soup)
            self.initMarketCap()

        except Exception as e:
            self.OK = False
            self.error = str(e)

        if self.not_valid() and self.error is None:
            self.OK = False
            self.dataValid = False

    def not_valid(self):
        # slightly laborious checking of attributes
        if len(self.AnnualRD) == 0: return True
        if len(self.OI) == 0: return True
        if len(self.assets) == 0: return True
        if len(self.debt) == 0: return True
        if self.MarketCap == 0: return True

    def getParsedHTML(self):

        URL_ROOT = "https://www.google.com/finance?fstype=ii&q="
        URL_TOT = URL_ROOT + self.exchange + "%3A" + self.ticker
        response = requests.get(URL_TOT)
        return bs4.BeautifulSoup(response.text)

    def getLineItem(self, soup, lineItem, rank):

        target = soup.find_all(name="td", text=re.compile(lineItem))[rank]

        results = []
        for node in target.next_siblings:
            s = node.string

            if s != '\n':
                if s == '-':
                    s = "0"
                s = s.replace(',', '')
                results.append(float(s))

        return results

    def initBS(self, soup):

        self.assets = self.getLineItem(soup, "Total Assets", 0)
        self.debt = self.getLineItem(soup, "Total Debt", 0)

        CSE = self.getLineItem(soup, "Cash and Short Term Investments", 0)
        LTI = self.getLineItem(soup, "Long Term Investments", 0)

        self.cash = [sum(i) for i in zip(CSE,LTI)]

    def initPL(self, soup):

        self.OI = self.getLineItem(soup, "Operating Income", 0)
        self.AnnualRD = self.getLineItem(soup, "Research & Development", 1)

    def initMarketCap(self):

        URL_ROOT = "https://www.google.com/finance?q="
        URL_TOT = URL_ROOT + self.exchange + "%3A" + self.ticker
        response = requests.get(URL_TOT)
        soup = bs4.BeautifulSoup(response.text)

        target = soup.find_all(name="table", class_="snap-data")

        elements = list(target[0].children)
        MC_group = elements[9].contents

        raw = MC_group[3].contents[0]

        p = re.compile('[M]*[B]*')
        raw_mc = float(p.split(raw)[0])

        if 'B' in p.findall(raw):
            mult = 1000.0
        else:
            mult = 1.0

        self.MarketCap = raw_mc * mult

    def calcROIC(self, amort):

        if amort==0:
            RD_add_back = 0
        else:
            RD_add_back = self.AnnualRD[0]

        # sum quarterly OI to get annual; add back last year's R&D
        adj_OI = sum(self.OI[0:3]) + RD_add_back
        
        # average assets + R&D asset
        adj_IC = sum(self.assets[0:3])/len(self.assets[0:3]) + self.calcRDAsset(amort)

        return round(adj_OI/adj_IC,2)

    def calcRDAsset(self, amort):
        
        # the no R&D asset case        
        if amort==0:
            return 0
            
        # amortization factors
        amort_factors = [(1-i/amort) for i in range(0,amort)]

        # get average over last x years
        ave_RD = int(sum(self.AnnualRD)/len(self.AnnualRD))

        # create an R&D list of the same length as amort_factors
        full_RD = []
        for i in range(0,amort):
            if i < len(self.AnnualRD):
                full_RD.append(self.AnnualRD[i])
            else:
                full_RD.append(ave_RD)
   
        RD_asset = []

        # get R&D asset value for full R&D
        for i, fac in enumerate(amort_factors):
            RD_asset.append(fac * full_RD[i])
        
        return sum(RD_asset)

    def calcMS(self, amort):

        # Numerator: Market Cap + Debt (latest)
        Num = self.MarketCap + self.debt[0]

        # Denominator: Total Assets (latest) + R&D asset
        Den = self.assets[0] + self.calcRDAsset(amort)

        return round(Num/Den,2)

    # Just a method for testing
    def printSelf(self):

        print(self.ticker)
        print("Ave Assets:")
        print(int(sum(self.assets)/len(self.assets)))
        print("Ave Debt:")
        print(int(sum(self.debt)/len(self.debt)))
        print("Ave Annual R&D: ")
        print(int(sum(self.AnnualRD)/len(self.AnnualRD)))
        print("Trailing 12-month OI:")
        print(sum(self.OI))
        print("Market Cap: ")
        print(self.MarketCap)
        print("R&D Asset(5): ")
        print(int(self.calcRDAsset(5)))
        print("R&D Asset(10): ")
        print(int(self.calcRDAsset(10)))
        print("MS(0): ")
        print(round(self.calcMS(0),2))
        print("MS(5): ")
        print(round(self.calcMS(5),2))
        print("MS(10): ")
        print(round(self.calcMS(10),2))
        print("ROIC(0): ")
        print(round(self.calcROIC(0),2))
        print("ROIC(5): ")
        print(round(self.calcROIC(5),2))
        print("ROIC(10): ")
        print(round(self.calcROIC(10),2))


