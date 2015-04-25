__author__ = 'petermarschel'

#import Inv_Tools
import csv

#TARG_1 = Inv_Tools.Company("IBM")
#TARG_2 = Inv_Tools.Company("!23FT$$")

#print(TARG_1.OK)
#print(TARG_2.OK)

csvfile = open('out.csv', 'w', newline='')
CSV_writer = csv.writer(csvfile, delimiter=',')

CSV_writer.writerow([23,46,78])
CSV_writer.writerow([47,33,12])
