__author__ = 'petermarschel'

import requests
import bs4
import re
import datetime

class Company:

    def __init__(self, ticker):

        self.ticker = ticker

        self.debt = 0
        self.assets = 0
        self.OI = 0
        self.AnnualRD = 0

        self.dates=[]

        self.MarketCap = 0

        try:
            self.initBS()
            self.initPL()
            self.initMarketCap()
        except:
            self.OK = False
        else:
            self.OK = True


    def initBS(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/bs?s="
        response = requests.get(URL_ROOT + self.ticker)
        soup = bs4.BeautifulSoup(response.text)

        self.processAssets(soup)
        self.processDebt(soup)
        self.processDates(soup)


    def initPL(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/is?s="
        response = requests.get(URL_ROOT + self.ticker)
        soup = bs4.BeautifulSoup(response.text)

        self.processOI(soup)
        
        RD_ROOT = "http://finance.yahoo.com/q/is?s="
        response = requests.get(RD_ROOT + self.ticker + "&annual")
        soup = bs4.BeautifulSoup(response.text)
        
        self.processAnnualRD(soup)


    def initMarketCap(self):

        URL_ROOT = "http://finance.yahoo.com/q?s="
        response = requests.get(URL_ROOT + self.ticker)
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

        return round(adj_OI/adj_IC,2)

    def calcRDAsset(self, amort):
        
        # the no R&D asset case        
        if amort==0:
            return 0
            
        # amortization factors
        amort_factors = [(1-i/amort) for i in range(0,amort)]

        # get average over last 3 years
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
        #print("Updated: " + self.updated)
        print("Latest Report Date:")
        print(self.dates[0])
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
        