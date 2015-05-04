__author__ = 'petermarschel'


import Inv_Tools
import Inv_Tools_Bio
from pprint import pprint

tick = "ACST"

TARG = Inv_Tools_Bio.Bio_Company(tick)
pprint (vars(TARG))

print(TARG.OK)
print(TARG.error)






