#!/usr/bin/python

import sys
import re
import csv
import traceback

from operator import itemgetter

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 11:
    print(
        "usage: " + program_name + " <debug_level : 1-4> <plan-list.csv> <reco-list.csv> <add.csv> <rmv.csv> <keep.csv>")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_filename_1 = sys.argv[2]
in_filename_2 = sys.argv[3]
in_filename_3 = sys.argv[4]
in_filename_4 = sys.argv[5]

out_filename_1 = sys.argv[6]
out_filename_2 = sys.argv[7]
out_filename_3 = sys.argv[8]
out_filename_4 = sys.argv[9]
out_filename_5 = sys.argv[10]

print('debug level :', debug_level)

if debug_level > 1:
    print('args :', len(sys.argv))

user_dict = {}
screener_buy_dict = {}
screener_hold_dict = {}
screener_sale_dict = {}
screener_hold_ratio_name_dict = {}
screener_hold_ratio_value_dict = {}
screener_sale_ratio_name_dict = {}
screener_sale_ratio_value_dict = {}

# user : ticker_list
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
            ticker = row[0]
            user_dict[ticker] = 1

# buy tickers
with open(in_filename_2, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        ticker = row[0]
        screener_buy_dict[ticker] = 1

# hold ticker with cause
with open(in_filename_3, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        ticker_name = row[0]
        ticker_reco = row[1]
        ratio_name = row[2]
        ratio_value = row[3]
        screener_hold_dict[ticker_name] = 1
        screener_hold_ratio_name_dict[ticker_name] = ratio_name
        screener_hold_ratio_value_dict[ticker_name] = ratio_value

# sale ticker with cause
with open(in_filename_4, 'rt') as csvfile:
    # future
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # fix the stripping : redundant spaces etc
        row = [column.strip() for column in row]
        ticker_name = row[0]
        ticker_reco = row[1]
        ratio_name = row[2]
        ratio_value = row[3]
        screener_sale_dict[ticker_name] = 1
        screener_sale_ratio_name_dict[ticker_name] = ratio_name
        screener_sale_ratio_value_dict[ticker_name] = ratio_value

if debug_level > 0:
    print("user dictionary", len(user_dict));
if debug_level > 1:
    print(user_dict)

if debug_level > 0:
    print("screener buy dictionary", len(screener_buy_dict));
if debug_level > 1:
    print(screener_buy_dict)

if debug_level > 0:
    print("screener hold ratio name dictionary", len(screener_hold_ratio_name_dict));
    print("screener hold ratio value dictionary", len(screener_hold_ratio_name_dict));
if debug_level > 1:
    print(screener_hold_ratio_name_dict)
    print(screener_hold_ratio_value_dict)

if debug_level > 0:
    print("screener sale ratio name dictionary", len(screener_sale_ratio_name_dict));
    print("screener sale ratio value dictionary", len(screener_sale_ratio_name_dict));
if debug_level > 1:
    print(screener_sale_ratio_name_dict)
    print(screener_sale_ratio_value_dict)

# sale
fh = open(out_filename_1, "w")
for ticker in user_dict:
    if ticker not in screener_buy_dict and ticker not in screener_hold_dict:
        if ticker in screener_sale_dict:
            line_ticker = ticker + ', ' + screener_sale_ratio_name_dict[ticker] + ', ' + screener_sale_ratio_value_dict[
                ticker] + '\n'
            fh.write(line_ticker)
fh.close()

# buy_new
fh = open(out_filename_2, "w")
for ticker in screener_buy_dict:
    if ticker not in user_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

# buy_more
fh = open(out_filename_3, "w")
for ticker in user_dict:
    if ticker in screener_buy_dict:
        line_ticker = ticker + '\n'
        fh.write(line_ticker)
fh.close()

# hold
fh = open(out_filename_4, "w")
for ticker in user_dict:
    if ticker in screener_hold_dict:
        line_ticker = ticker + ', ' + screener_hold_ratio_name_dict[ticker] + ', ' + screener_hold_ratio_value_dict[
            ticker] + '\n'
        fh.write(line_ticker)
fh.close()

# missing data
fh = open(out_filename_5, "w")
for ticker in user_dict:
    if ticker not in screener_buy_dict and ticker not in screener_hold_dict and ticker not in screener_sale_dict:
        line_ticker = ticker + ', missing data, ?' + '\n'
        fh.write(line_ticker)
fh.close()
