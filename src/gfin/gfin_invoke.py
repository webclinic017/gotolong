#!/usr/bin/python

import sys
import re
import csv
import traceback
import gfin

from operator import itemgetter

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

args = parser.parse_args()

debug_level = args.debug_level

# dummy assignment
out_filename_phase = []
for index, filename in enumerate(args.out_files):
    print('index = ', index, filename);
    out_filename_phase.append(filename)

# Main caller
program_name = sys.argv[0]

# debug_level = int(sys.argv[1])
# in_plan_filename = sys.argv[2]
# out_filename_phase1 = sys.argv[3]
# out_filename_phase2 = sys.argv[4]
# out_filename_phase3 = sys.argv[5]
# out_filename_phase4 = sys.argv[6]
# out_filename_phase5 = sys.argv[7]

if debug_level > 1:
    print('args :', len(sys.argv))

gfin = gfin.Gfin()

gfin.set_debug_level(debug_level)

gfin.amfi_load_db()
gfin.isin_load_db()
gfin.screener_load_db()
gfin.trendlyne_load_db()

gfin.gfin_dump_report(out_filename_phase[0], out_filename_phase[1])
