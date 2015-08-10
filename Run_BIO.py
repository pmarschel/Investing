__author__ = 'pemarsc'

import csv
import Inv_Tools_Bio
import time

start = time.time()

with open('Company_List_BIO.csv') as f:
    #"/home/pmarschel/Investing/Invest_Out/out_BIO_" + time.strftime("%d_%m_%Y") + ".csv"
    reader = csv.reader(f)
    tick_list = list(reader)

out_file_name = "../Invest_out/out_BIO_" + time.strftime("%d_%m_%Y") + ".csv"
    #"/home/pmarschel/Investing/Invest_Out/out_BIO_" + time.strftime("%m_%d_%Y") + ".csv"

csvfile = open(out_file_name, 'w', newline='')
CSV_writer = csv.writer(csvfile, delimiter=',')

CSV_writer.writerow(["Ticker", "Market_Cap", "Debt", "RD(10)", "RD(15)", "MS(10)", "MS(15)", "Inst_Own", "OI_cov"])

num_processed = 0

for tick in tick_list:

    comp = Inv_Tools_Bio.Bio_Company(tick[0])
    num_processed += 1
    print(str(num_processed) + ": " + tick[0])

    if comp.OK:
        if comp.passScreen(ms15_lim = 1.2, OIcov_lim = 1.5, instOwn_lim = 50):
            CSV_writer.writerow([comp.ticker,
                             comp.MarketCap,
                             comp.debt[0],
                             round(comp.calcRDAsset(10)/1000,2),
                             round(comp.calcRDAsset(15)/1000,2),
                             comp.calcMS(10),
                             comp.calcMS(15),
                             comp.InstOwn,
                             comp.calcOICov()])
    else:
        CSV_writer.writerow([comp.ticker,
                             comp.error])

csvfile.close()

end = time.time()

hours = str(round((end - start)/3600,2))

print("Time elapsed(hours): " + hours)


