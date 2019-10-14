#!/usr/bin/python

import sys
import re
import csv
import traceback

import demat

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 6:
    print("usage: " + program_name + " <debug_level : 1-4> <demat.csv> ... ")
    sys.exit(1)

debug_level = int(sys.argv[1])
txn_file = sys.argv[2]
summary_file = sys.argv[3]
out_file_1 = sys.argv[4]
out_file_2 = sys.argv[5]
out_file_3 = sys.argv[6]
out_file_4 = sys.argv[7]
out_file_5 = sys.argv[8]

if debug_level > 1:
    print('args :', len(sys.argv))

demat = demat.Demat()

demat.set_debug_level(debug_level)

demat.amfi_load_db()
demat.demat_txn_load_data(txn_file)
demat.demat_summary_load_data(summary_file)
demat.print_phase1(out_file_1)
demat.print_phase2(out_file_2)
demat.print_phase3(out_file_3)
demat.print_phase4(out_file_4)
demat.print_phase5(out_file_5)
