#!/usr/bin/python

import sys
import re
import csv
import traceback
import trendlyne

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

trendlyne = trendlyne.Trendlyne()

trendlyne.set_debug_level(debug_level)

if truncate_table:
    trendlyne.trendlyne_table_reload(truncate_table)

trendlyne.amfi_load_db()

trendlyne.trendlyne_load_data(in_filename_phase[0])
trendlyne.trendlyne_dump(out_filename_phase[0])
