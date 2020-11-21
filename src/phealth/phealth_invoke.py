#!/usr/bin/python

import sys
import re
import csv
import traceback
import phealth

from operator import itemgetter

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

args = parser.parse_args()

debug_level = args.debug_level
log_level = args.log_level

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

phealth = phealth.Phealth()

phealth.set_log_level(log_level)

phealth.set_debug_level(debug_level)

phealth.amfi_load_data_from_db()
phealth.isin_load_db()
phealth.screener_load_db()
phealth.trendlyne_load_db()
phealth.demat_txn_load_db()
phealth.demat_sum_load_db()
phealth.gweight_load_db()
phealth.bhav_load_data_from_db()
phealth.ftwhl_load_data_from_db()
phealth.corpact_load_data_from_db()

phealth.phealth_dump_report(out_filename_phase[0], out_filename_phase[1])
