#!/usr/bin/python

import sys
import re
import csv
import traceback

import demat

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('-t', '--truncate_table', default='False', help='truncate table', action='store_true')
parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

args = parser.parse_args()

debug_level = args.debug_level
truncate_table = args.truncate_table

# dummy assignment
in_filename_phase = []
out_filename_phase = []
# use the argument as pattern
for index, filename in enumerate(args.in_files):
    print('index = ', index, filename);
    in_filename_phase.append(filename)

for index, filename in enumerate(args.out_files):
    print('index = ', index, filename);
    out_filename_phase.append(filename)

# Main caller
program_name = sys.argv[0]

# if len(sys.argv) < 6:
#    print("usage: " + program_name + " <debug_level : 1-4> <demat.csv> ... ")
#    sys.exit(1)

# debug_level = int(sys.argv[1])
# txn_file = sys.argv[2]
# summary_file = sys.argv[3]
# out_file_1 = sys.argv[4]
# out_file_2 = sys.argv[5]
# out_file_3 = sys.argv[6]
# out_file_4 = sys.argv[7]
# out_file_5 = sys.argv[8]

txn_file = in_filename_phase[0]
summary_file = in_filename_phase[1]

if debug_level > 1:
    print('args :', len(sys.argv))

demat = demat.Demat()

demat.set_debug_level(debug_level)

if truncate_table:
    demat.demat_table_reload(truncate_table)

demat.amfi_load_db()
demat.demat_txn_load_data(txn_file)
demat.demat_summary_load_data(summary_file)
demat.demat_dump_txn_detailed(out_filename_phase[0])
demat.demat_dump_txn_compressed(out_filename_phase[1])
demat.demat_dump_txn_summary(out_filename_phase[2])
# positive holdings
demat.demat_dump_txn_summary(out_filename_phase[3], True)
demat.demat_dump_summary_ticker_only(out_filename_phase[4])
demat.demat_dump_summary_captype(out_filename_phase[5])
demat.demat_dump_holdings_by_rank(out_filename_phase[6])
