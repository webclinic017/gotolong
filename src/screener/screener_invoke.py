#!/usr/bin/python

import sys
import re
import csv
import traceback
import screener

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

if debug_level > 1:
    print('args :', len(sys.argv))

	
if debug_level > 1 :
	print('args :' , len(sys.argv))

screener = screener.Screener()

screener.set_debug_level(debug_level)

if truncate_table:
    screener.screener_table_reload(truncate_table)

screener.amfi_load_db()
screener.isin_load_db()
# screener.load_amfi_data(in_amfi_filename)

screener.screener_load_data(in_filename_phase[0])

screener.screener_dump_phase1(out_filename_phase[0])
screener.screener_dump_phase2(out_filename_phase[1])
screener.screener_dump_phase3(out_filename_phase[2], out_filename_phase[3], out_filename_phase[4],
                              out_filename_phase[5], out_filename_phase[6])
