#!/usr/bin/python

import sys
import re
import csv
import traceback
import isin

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 5:
    print("usage: " + program_name + " <debug_level : 1-4> <isin.csv> ... ")
    sys.exit(1)

debug_level = int(sys.argv[1])
bse_filename = sys.argv[2]
nse_filename = sys.argv[3]
out_filename_1 = sys.argv[4]
out_filename_2 = sys.argv[5]

if debug_level > 1 :
    print('args :' , len(sys.argv))

isin = isin.Isin()

isin.set_debug_level(debug_level)

# isin.load_isin_data(bse_filename, 'bse')
isin.isin_load_data(nse_filename, 'nse')

isin.isin_dump_report_full(out_filename_1)
isin.isin_dump_report_industry_only(out_filename_2)
