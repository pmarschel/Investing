__author__ = 'petermarschel'


import requests
import bs4
import re
import Inv_Tools

class Bio_Company(Inv_Tools.Company):

    def __init__(self, ticker):

        super(Bio_Company, self).__init__(ticker)

        self.InstOwn = 0
        self.cash = []

        try:
            self.initInstOwn()
            self.initCash()

        except Exception as e:
            self.OK = False
            self.error = str(e)

        if self.not_valid_BIO():
            self.OK = False
            self.error = "Data Invalid"

    def not_valid_BIO(self):
        # slightly laborious checking of attributes
        if len(self.cash) == 0: return True

    def initInstOwn(self):

        URL_ROOT = "http://finance.yahoo.com/q/ks?s="
        response = requests.get(URL_ROOT + self.ticker)
        soup = bs4.BeautifulSoup(response.text)

        # Process the HTML to get prev close
        start_html = soup.find_all(name="td", text=re.compile('Float'))

        target = start_html[0]
        target = target.parent.next_sibling.next_sibling
        raw = target.contents[1].string

        if raw == 'N/A':
            inst_own = None
        else:
            inst_own = float(raw[0:3])

        self.InstOwn = inst_own

    def initCash(self):

        # Get the balance sheet
        URL_ROOT = "http://finance.yahoo.com/q/bs?s="
        response = requests.get(URL_ROOT + self.ticker)
        soup = bs4.BeautifulSoup(response.text)

        # Process the HTML to get cash, short term investments, long term investments
        cash_html = soup.find_all(name="td", text=re.compile("Cash And Cash Equivalents"))
        short_inv_html = soup.find_all(name="td", text=re.compile("Short Term Investments"))
        long_inv_html = soup.find_all(name="td", text=re.compile("Long Term Investments"))

        cash = self.processRow(cash_html[0])
        short_inv = self.processRow(short_inv_html[0])
        long_inv = self.processRow(long_inv_html[0])

        total_cash = [sum(i) for i in zip(cash,short_inv, long_inv)]

        self.cash = total_cash

    def calcOICov(self):

        curr_cash = self.cash[0]
        OI_ann = sum(self.OI)

        if OI_ann == 0:
            return -10
        else:
            return -round(curr_cash/OI_ann,2)