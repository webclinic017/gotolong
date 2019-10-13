#!/usr/bin/python

import sys
import re
import csv
import traceback

import demat_summary

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 5:
    print
    "usage: " + program_name + " <debug_level : 1-4> <demsum.csv> ... "
    sys.exit(1)

debug_level = int(sys.argv[1])
in_file_1 = sys.argv[2]
in_file_2 = sys.argv[3]
out_file_1 = sys.argv[4]
out_file_2 = sys.argv[5]

if debug_level > 1:
    print
    'args :', len(sys.argv)

demsum = demat_summary.DemSum()

demsum.set_debug_level(debug_level)
demsum.load_demsum_data(in_file_1, 'icicidirect')
demsum.load_demsum_data(in_file_2, 'zerodha')
demsum.print_phase1(out_file_1)
demsum.print_phase2(out_file_2)
