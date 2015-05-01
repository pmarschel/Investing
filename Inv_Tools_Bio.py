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
        else:
            self.OK = True
            self.error = None

    def initInstOwn(self):

        URL_ROOT = "http://finance.yahoo.com/q/ks?s="
        response = requests.get(URL_ROOT + self.ticker)
        soup = bs4.BeautifulSoup(response.text)

        # Process the HTML to get prev close
        start_html = soup.find_all(name="td", text=re.compile('Float'))

        target = start_html[0]
        target = target.parent.next_sibling.next_sibling
        raw = target.contents[1].string

        inst_own = float(raw[0:3])

        self.InstOwn = inst_own