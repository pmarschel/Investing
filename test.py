__author__ = 'petermarschel'

import Inv_Tools

tick = "IBM"


TARG = Inv_Tools.Company(tick)

print(TARG.OK)
print(TARG.OI)
print(TARG.calcROIC(10))
