__author__ = 'petermarschel'

import Inv_Tools

tick = "IBM"

TARG = Inv_Tools.Company(tick)

TARG.printSelf()

print(TARG.calcRDAsset(5))
print(TARG.calcRDAsset(15))

print(TARG.calcMS(5))
print(TARG.calcMS(15))

print(TARG.calcROIC(5))
print(TARG.calcROIC(15))