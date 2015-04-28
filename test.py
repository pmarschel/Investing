__author__ = 'petermarschel'

import Inv_Tools

tick = "VNET"


TARG = Inv_Tools.Company(tick)

print(TARG.OK)
print(TARG.error)