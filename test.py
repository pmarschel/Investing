__author__ = 'petermarschel'

import Inv_Tools

tick = "WTT"


TARG = Inv_Tools.Company(tick)

print(TARG.OK)
print(TARG.error)

print(TARG.OI)
print(TARG.assets)
print(TARG.calcROIC(0))