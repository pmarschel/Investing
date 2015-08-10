__author__ = 'petermarschel'


import requests
import bs4
import re
import Inv_Tools

class Bio_Company(Inv_Tools.Company):

    def __init__(self, ticker):

        super(Bio_Company, self).__init__(ticker)

        self.InstOwn = 0

        try:
            self.initInstOwn()

        except Exception as e:
            self.OK = False
            self.error = str(e)

    def initInstOwn(self):

        URL_ROOT = "https://www.google.com/finance?q="
        URL_TOT = URL_ROOT + self.exchange + "%3A" + self.ticker
        response = requests.get(URL_TOT)
        soup = bs4.BeautifulSoup(response.text)

        target = soup.find_all(name="table", class_="snap-data")

        elements = list(target[1].children)
        IO_group = elements[9].contents

        raw = IO_group[3].contents[0]
        p = re.compile('[%]')

        if '%' in raw:
            self.InstOwn = int(p.split(raw)[0])

    def calcOICov(self):

        curr_cash = self.cash[0]
        OI_ann = sum(self.OI)

        if OI_ann == 0:
            return -10
        else:
            return -round(curr_cash/OI_ann,2)

    def passScreen(self, ms15_lim, OIcov_lim, instOwn_lim):

        if self.InstOwn < instOwn_lim:
            return False
        elif self.calcOICov() < OIcov_lim:
            return False
        elif self.calcMS(15) > ms15_lim:
            return False
        else:
            return True