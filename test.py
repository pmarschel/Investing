__author__ = 'petermarschel'

import Inv_Tools
import time
import statistics as stat



hold=[]
tick = "MSFT"

for i in range(0,200):
    start_int = time.clock()
    TARG = Inv_Tools.Company(tick)
    end_int = time.clock()
    hold.append(end_int - start_int)
    print(i)

print(round(stat.mean(hold),2))
print(round(stat.stdev(hold),2))




#TARG.printSelf()
#print(TARG.AnnualRD)
#print(TARG.calcRDAsset(5))
#print(TARG.AnnualRD)


#print(TARG.calcMS(5))
#print(TARG.calcMS(15))

#print(TARG.calcROIC(5))
#print(TARG.calcROIC(15))