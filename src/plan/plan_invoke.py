#!/usr/bin/python

import sys
import re
import csv
import traceback
import plan

from operator import itemgetter

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('--truncate_table', default='False', help='specify to truncate', action='store_true')
parser.add_argument('--in_files', nargs='+', dest='in_files', help='in files')
parser.add_argument('--out_files', nargs='+', dest='out_files', help='out files')

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

if len(sys.argv) < 6 :
    print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> <plan.csv> ... ")
    sys.exit(1)

# debug_level = int(sys.argv[1])
# in_plan_filename = sys.argv[2]
# out_filename_phase1 = sys.argv[3]
# out_filename_phase2 = sys.argv[4]
# out_filename_phase3 = sys.argv[5]
# out_filename_phase4 = sys.argv[6]
# out_filename_phase5 = sys.argv[7]

if debug_level > 1 :
    print('args :', len(sys.argv))

indu_comp = 'comp'
ic_name = 'all'

if len(sys.argv) == 9 :
    indu_comp = sys.argv[5]
    ic_name = sys.argv[6]
    ic_name = ic_name.capitalize()

plan = plan.Plan()

plan.set_debug_level(debug_level)

if truncate_table:
    plan.set_table_reload(truncate_table)

plan.load_amfi_db()
plan.load_plan_data(in_filename_phase[0])

plan.plan_dump_ticker(out_filename_phase[0])
plan.plan_dump_sorted_units(out_filename_phase[1])
plan.plan_dump_all(out_filename_phase[2])
plan.plan_dump_plus(out_filename_phase[3])
plan.plan_dump_zero(out_filename_phase[4])

if len(sys.argv) == 8 :
    if indu_comp.lower() == "comp":
        print('companies count : ', plan.size_comp_data())
        if ic_name == "All":
            plan.print_comp_data()
        else:
            print(plan.get_plan_comp_units(ic_name))
    else:
        print('industries count : ', plan.size_indu_data())
        if ic_name == "All":
            plan.print_indu_data()
        else:
            print(plan.get_indu_units(ic_name))
