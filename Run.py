__author__ = 'petermarschel'


import csv
with open('Company_List.csv') as f:
    reader = csv.reader(f)
    comp_list = list(reader)

print(comp_list[0:10])
