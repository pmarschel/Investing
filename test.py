__author__ = 'petermarschel'


import Inv_Tools
import Inv_Tools_Bio
from pprint import pprint

tick = "WTT"

TARG = Inv_Tools.Company(tick)
pprint (vars(TARG))

print(TARG.OK)
print(TARG.error)

print(TARG.calcMS(0))
#print(sum(TARG.OI))
#print(TARG.cash)
#print(TARG.calcOICov())




