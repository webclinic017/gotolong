#!/usr/bin/python

import sys
import re
import csv
import traceback

from operator import itemgetter

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 8:
    print(
        "usage: " + program_name + " <debug_level : 1-4> <plan-list.csv> <reco-list.csv> <add.csv> <rmv.csv> <keep.csv>")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_filename_1 = sys.argv[2]
in_filename_2 = sys.argv[3]
in_filename_3 = sys.argv[4]
out_filename_1 = sys.argv[5]
out_filename_2 = sys.argv[6]
out_filename_3 = sys.argv[7]

print('debug level :', debug_level)

if debug_level > 1:
    print('args :', len(sys.argv))

user_dict = {}
screener_accept_dict = {}
screener_reject_ratio_name_dict = {}
screener_reject_ratio_value_dict = {}


with open(in_filename_1, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        if debug_level > 2:
            print("debugging: blank row")
            print(row)
        if len(row) != 0:
            column = row[0]
            user_dict[column] = 1

with open(in_filename_2, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        column = row[0]
        screener_accept_dict[column] = 1

with open(in_filename_3, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        ticker_name = row[0]
        ratio_name = row[1]
        ratio_value = row[2]
        screener_reject_ratio_name_dict[ticker_name] = ratio_name
        screener_reject_ratio_value_dict[ticker_name] = ratio_value

if debug_level > 0:
    print("user dictionary", len(user_dict));
if debug_level > 1:
    print(user_dict)

if debug_level > 0:
    print("screener accepted dictionary", len(screener_accept_dict));
if debug_level > 1:
    print(screener_accept_dict)

if debug_level > 0:
    print("screener rejected ratio name dictionary", len(screener_reject_ratio_name_dict));
    print("screener rejected ratio value dictionary", len(screener_reject_ratio_name_dict));
if debug_level > 1:
    print(screener_reject_ratio_name_dict)
    print(screener_reject_ratio_value_dict)


fh = open(out_filename_1, "w")
for ticker in user_dict:
    if ticker not in screener_accept_dict:
        if ticker in screener_reject_ratio_name_dict and ticker in screener_reject_ratio_value_dict:
            line_ticker = ticker + ', ' + screener_reject_ratio_name_dict[ticker]
            line_ticker = line_ticker + ', ' + screener_reject_ratio_value_dict[ticker] + '\n'
        else:
            line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

fh = open(out_filename_2, "w")
for ticker in screener_accept_dict:
    if ticker not in user_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

fh = open(out_filename_3, "w")
for ticker in user_dict:
    if ticker in screener_accept_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()
