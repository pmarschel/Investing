__author__ = 'petermarschel'

import Inv_Tools
import yahoo_finance

TARG = Inv_Tools.Company("AAPL")


print(TARG.getTicker())

print("Collected data")
print(TARG.getAssets())
print(TARG.getOI())
print(TARG.getAnnualRD())

print("Here's the ROIC")
print(TARG.getROIC())