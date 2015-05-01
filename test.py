__author__ = 'petermarschel'


import Inv_Tools
import Inv_Tools_Bio
from pprint import pprint

tick = "BIIB"

TARG = Inv_Tools_Bio.Bio_Company(tick)
pprint (vars(TARG))
print(vars(TARG).__class__)
print(TARG.OK)
print(TARG.error)
#print(sum(TARG.OI))
#print(TARG.cash)
#print(TARG.calcOICov())




