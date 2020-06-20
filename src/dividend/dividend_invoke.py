#!/usr/bin/python

import sys
import re
import csv
import traceback

import dividend

from operator import itemgetter

import glob
import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('-t', '--truncate_table', default='False', help='truncate table', action='store_true')
parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
parser.add_argument('-a', '--alias_files', required=True, nargs='+', dest='alias_files', help='alias files')
parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

args = parser.parse_args()

debug_level = args.debug_level
truncate_table = args.truncate_table

# dummy assignment
in_filename_phase = []
out_filename_phase = []
alias_filename_phase = []
# use the argument as pattern
for index, filename in enumerate(args.in_files):
    print('index = ', index, filename);
    in_filename_phase.append(filename)

for index, filename in enumerate(args.alias_files):
    print('index = ', index, filename);
    alias_filename_phase.append(filename)

for index, filename in enumerate(args.out_files):
    print('index = ', index, filename);
    out_filename_phase.append(filename)

# Main caller
program_name = sys.argv[0]

if debug_level > 1 :
    print('args :' , len(sys.argv))
    print('in_dividend_filenames :' + in_dividend_filenames)

if debug_level > 1:
    print('args :', len(sys.argv))

dividend = dividend.Dividend()

dividend.set_debug_level(debug_level)

if truncate_table:
    dividend.dividend_table_reload(truncate_table)

dividend.amfi_load_db()

dividend.dividend_load_aliases_data(alias_filename_phase[0])

# expand * for all
dividend.dividend_load_data(glob.glob(in_filename_phase[0]))

dividend.dividend_dump_orig(out_filename_phase[0])
dividend.dividend_print_phase1(out_filename_phase[1])
dividend.dividend_print_phase2(out_filename_phase[2])
dividend.dividend_print_phase3(out_filename_phase[3])
dividend.dividend_print_phase4(out_filename_phase[4])
dividend.dividend_print_phase5(out_filename_phase[5])
dividend.dividend_print_phase6(out_filename_phase[6])
