__author__ = 'petermarschel'

class Company:

    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name
        self.financials = []    # creates a new empty list for financials

    def set_financials(self):
        ## get financials here
        print("financials set")

    def rand_method(self):
        print("do some stuff")

    @property
    def get_ticker(self):
        return self.ticker

    @property
    def get_name(self):
        return self.name


'''some pointless change'''
