#!/usr/bin/python

import sys
import re
import csv
import traceback

from operator import itemgetter

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 7:
    print(
        "usage: " + program_name + " <debug_level : 1-4> <plan-list.csv> <reco-list.csv> <add.csv> <rmv.csv> <keep.csv>")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_filename_1 = sys.argv[2]
in_filename_2 = sys.argv[3]
out_filename_1 = sys.argv[4]
out_filename_2 = sys.argv[5]
out_filename_3 = sys.argv[6]

if debug_level > 1:
    print('args :', len(sys.argv))

screener_dict = {}
user_dict = {}

with open(in_filename_1, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        column = row[0]
        user_dict[column] = 1

with open(in_filename_2, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        column = row[0]
        screener_dict[column] = 1

if debug_level > 0:
    print("\nuser dictionary", len(user_dict));
    if debug_level > 1:
        print(user_dict)
    print("\nscreener dictionary", len(screener_dict));
    if debug_level > 1:
        print(screener_dict)

fh = open(out_filename_1, "w")
for ticker in user_dict:
    if ticker not in screener_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

fh = open(out_filename_2, "w")
for ticker in screener_dict:
    if ticker not in user_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

fh = open(out_filename_3, "w")
for ticker in user_dict:
    if ticker in screener_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()
