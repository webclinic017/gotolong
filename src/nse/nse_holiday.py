#!/usr/bin/python

import re
import datetime
import sys

debug = 0

today = datetime.date.today()

if debug > 0:
    print('year', today.year)

filename = sys.argv[1]

FH = open(filename)

for line in FH:
    date_column = line.split()[1]
    if re.findall(r"-", date_column):
        new_column = datetime.datetime.strptime(date_column, '%d-%b-%Y').strftime('%d%m%Y')
        print(new_column)
    else:
        if debug > 0:
            print('no match', date_column)

FH.close()
