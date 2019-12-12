#!/usr/bin/python

import sys
import re
import csv
import traceback
import dividend

from operator import itemgetter

import glob

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 7:
    print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> <dividend.csv> ... ")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_amfi_filename = sys.argv[2]
in_aliases_filename = sys.argv[3]
out_filename_phase0 = sys.argv[4]
out_filename_phase1 = sys.argv[5]
out_filename_phase2 = sys.argv[6]
out_filename_phase3 = sys.argv[7]
out_filename_phase4 = sys.argv[8]
out_filename_phase5 = sys.argv[9]
in_dividend_filenames = sys.argv[10]

if debug_level > 1 :
    print('args :' , len(sys.argv))
    print('in_dividend_filenames :' + in_dividend_filenames)

dividend = dividend.Dividend()

dividend.set_debug_level(debug_level)

dividend.amfi_load_db()
#dividend.load_amfi_data(in_amfi_filename)
dividend.load_aliases_data(in_aliases_filename)
# expand * for all
dividend.load_dividend_data(glob.glob(in_dividend_filenames))

dividend.dump_orig(out_filename_phase0)
dividend.print_phase1(out_filename_phase1)
dividend.print_phase2(out_filename_phase2)
dividend.print_phase3(out_filename_phase3)
dividend.print_phase4(out_filename_phase4)
dividend.print_phase5(out_filename_phase5)
