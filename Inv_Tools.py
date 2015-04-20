__author__ = 'petermarschel'

import requests
import bs4
import re
import datetime

class Company:

    def __init__(self, ticker):

        self.ticker = ticker
        self.updated = "some date"

        self.debt = 0
        self.assets = 0
        self.OI = 0
        self.AnnualRD = 0

        self.dates=[]

        self.MarketCap = 0

        self.initBS()
        self.initPL()
        self.initMarketCap()


    def getTicker(self):
        return self.ticker

    def getUpdated(self):
        return self.updated

    def getDebt(self):
        return self.debt

    def getAssets(self):
        return self.assets
        
    def getOI(self):
        return self.OI
        
    def getAnnualRD(self):
        return self.AnnualRD

    def getDates(self):
        return self.dates

    def getMarketCap(self):
        return self.MarketCap


    def initBS(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/bs?s="
        response = requests.get(URL_ROOT + self.getTicker())
        soup = bs4.BeautifulSoup(response.text)

        self.processAssets(soup)
        self.processDebt(soup)
        #self.processDates(soup)


    def initPL(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/is?s="
        response = requests.get(URL_ROOT + self.getTicker())
        soup = bs4.BeautifulSoup(response.text)

        self.processOI(soup)
        
        RD_ROOT = "http://finance.yahoo.com/q/is?s="
        response = requests.get(RD_ROOT + self.getTicker() + "&annual")
        soup = bs4.BeautifulSoup(response.text)
        
        self.processAnnualRD(soup)


    def initMarketCap(self):

        URL_ROOT = "http://finance.yahoo.com/q?s="
        response = requests.get(URL_ROOT + self.getTicker())
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

        self.MarketCap = int(raw_mc * mult)


    def processAssets(self, soup):

        # Process the HTML to get total assets
        tot_assets = soup.find_all(name="strong", text=re.compile("Total Assets"))
        target = tot_assets[0]
        parent = target.parent.parent

        p=re.compile('[0-9]*')
        temp = []

        for node in parent.contents:

            # raw contents
            raw_contents = ''.join(node.contents[1])

            # get numbers separated by ,
            nums=p.findall(raw_contents)

            # stick the nums together to get one big num
            assets = ''.join(nums)

            # put them in the list
            temp.append(assets)

        # turn list to int and assign to member variable
        results = [int(i) for i in temp[1:]]
        self.assets = results


    def processDebt(self, soup):

        # Process the HTML to get STD and LTD
        tot_debt = soup.find_all(name="td", text=re.compile("Long Term Debt"))

        STD = self.debtTarget(tot_debt[0])
        LTD = self.debtTarget(tot_debt[1])

        DEBT = [sum(i) for i in zip(STD,LTD)]

        self.debt = DEBT


    def debtTarget(self, target):

        p=re.compile('[0-9]*')

        result = []

        for i in range(4):
            target = target.next_sibling
            result.append(''.join(p.findall(target.string)))

        result = [ '0' if x == '' else x for x in result ]

        return([int(i) for i in result])


    def processDates(self, soup):

        td = soup.find_all(name="td", text=re.compile("Period Ending"))
        target = td[0]

        dates = []

        for i in range(4):
            target = target.next_sibling
            dates.append(datetime.datetime.strptime(target.string, '%b %d, %Y').date())

        self.dates = dates
        
    
    def processOI(self, soup):

        # Process the HTML to get OI
        OI = soup.find_all(name="strong", text=re.compile("Operating Income or Loss"))
        target = OI[0]
        parent = target.parent.parent

        p=re.compile('[0-9]*')
        temp = []

        for node in parent.contents:

            # raw contents
            raw_contents = ''.join(node.contents[1])

            # get numbers separated by ,
            nums=p.findall(raw_contents)

            # stick the nums together to get one big num
            assets = ''.join(nums)

            # put them in the list
            temp.append(assets)

        # turn list to int and assign to member variable
        results = [int(i) for i in temp[1:]]
        self.OI = results
    
    def processAnnualRD(self, soup):
        
        std = soup.find_all(name="td", text=re.compile("Research Development"))
        target = std[0]

        sibs = target.next_siblings

        p=re.compile('[0-9]*')
        result = []

        for sib in sibs:
            result.append(''.join(p.findall(sib.string)))

        result = [ '0' if x == '' else x for x in result ]
        result = [int(i) for i in result]

        self.AnnualRD = result

    def calcROIC(self, amort):
        
        # sum quarterly OI to get annual; add back last year's R&D
        adj_OI = sum(self.OI) + self.AnnualRD[0]
        
        # average assets + R&D asset
        adj_IC = sum(self.assets)/len(self.assets) + self.calcRDAsset(amort)

        return adj_OI/adj_IC

    def calcRDAsset(self, amort):

        # start the RD sequence with numbers we already have
        RD = self.AnnualRD

        # get average over last 3 years
        ave_RD = int(sum(RD)/len(RD))

        # fill out the rest of the RD sequence
        for i in range(0, amort-len(RD)):
            RD.append(ave_RD)

        # do straight-line amortization
        for i, val in enumerate(RD):
            RD[i] = int(val*(1 - i / amort))

        return sum(RD)

    def calcMS(self, amort):

        # Numerator: Market Cap + Debt (latest)
        Num = self.MarketCap + self.debt[0]

        # Denominator: Total Assets (latest) + R&D asset
        Den = self.assets[0] + self.calcRDAsset(amort)

        return round(Num/Den,7)

    # Just a method for testing
    def printSelf(self):

        print(self.getTicker())
        print("Updated: " + self.getUpdated())
        print("Total Assets:")
        print(self.getAssets())
        print("Debt:")
        print(self.getDebt())
        print("Dates:")
        print(self.getDates())
        print("Annual R&D:")
        print(self.getAnnualRD())
        print("OI:")
        print(self.getOI())
        print("Market Cap:")
        print(self.getMarketCap())