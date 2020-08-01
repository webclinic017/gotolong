#!/usr/bin/python

import sys
import re
import csv
import traceback
import amfi

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('-t', '--truncate_table', default='False', help='specify to truncate', action='store_true')
parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')
parser.add_argument('-s', '--save_to_db', default='True', help='save data to db', action='store_true')
parser.add_argument('-x', '--export_to_file', default='True', help='export data to file', action='store_true')
parser.add_argument('-p', '--pretty_dump', default='True', help='pretty dump', action='store_true')
args = parser.parse_args()

log_level = args.log_level
truncate_table = args.truncate_table
save_to_db = args.save_to_db
export_to_file = args.export_to_file
pretty_dump = args.pretty_dump

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

if len(sys.argv) < 4:
    print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> ... ")
    sys.exit(1)

print('args :', len(sys.argv))

amfi = amfi.Amfi()

amfi.set_log_level(log_level)

if truncate_table:
    amfi.amfi_table_reload(truncate_table)

if save_to_db:
    amfi.amfi_store_data_to_db(in_filename_phase[0])

amfi.amfi_load_data_from_db()

amfi.amfi_export(export_to_file, out_filename_phase[0])

amfi.amfi_dump(pretty_dump, out_filename_phase[1])
