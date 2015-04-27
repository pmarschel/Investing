__author__ = 'petermarschel'


import csv
import Inv_Tools
import time

start = time.time()

with open('Company_List.csv') as f:
    reader = csv.reader(f)
    tick_list = list(reader)

out_file_name = "../Invest_out/out_" + time.strftime("%d_%m_%Y") + ".csv"

csvfile = open(out_file_name, 'w', newline='')
CSV_writer = csv.writer(csvfile, delimiter=',')

CSV_writer.writerow(["Ticker","MS(0)", "ROIC(0)", "MS(5)", "ROIC(5)", "MS(10)", "ROIC(10)"])

num_processed = 0

for tick in tick_list[1:20]:

    comp = Inv_Tools.Company(tick[0])
    num_processed += 1
    print(num_processed)

    if comp.OK:
        CSV_writer.writerow([comp.ticker,
                             comp.calcMS(0),
                             comp.calcROIC(0),
                             comp.calcMS(5),
                             comp.calcROIC(5),
                             comp.calcMS(10),
                             comp.calcROIC(10)])
    else:
        CSV_writer.writerow([comp.error])

csvfile.close()

end = time.time()

hours = str(round((end - start)/3600,2))

print("Time elapsed(hours): " + hours)