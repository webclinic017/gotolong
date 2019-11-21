#!/usr/bin/python

# Input Template (equity-target-units.csv) file
# Ignore first 10 lines
# Each entry template
# Industry,Sub Industry, Company,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,TBD %,Last Date,


import sys
import re
import csv
from collections import Counter
from operator import itemgetter

import glob

import argparse

parser = argparse.ArgumentParser(description='Process arguments')
# dest= not required as option itself is the destination in args
parser.add_argument('--out_type', default='out_plain', help='out_plain | out_csv')
parser.add_argument('--sort_type', default='sort_frequency', help='sort_frequency')
parser.add_argument('--summary_type', default='summary_yes|summary_no', help='summary_yes')
parser.add_argument('--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
parser.add_argument('--dividend_file', nargs='+', dest='dividend_file', help='dividend file')
parser.add_argument('--bonus_file', nargs='+', dest='bonus_file', help='bonus file')
parser.add_argument('--buyback_file', nargs='+', dest='buyback_file', help='buyback file')

args = parser.parse_args()

# print(args)

program_name = sys.argv[0]

"""
if len(sys.argv) < 6 :
   print("usage: " + program_name + " <out_plain | out_csv> <sort_frequency| sort_frquency_name_only|sort_amount|company_name_only> <summary_yes|sumary_no> <debug_level : 1-4> <dividend-bse.csv> ... ")
   sys.exit(1)

out_type= sys.argv[1]
sort_type= sys.argv[2]
summary_type= sys.argv[3]
debug_level= int(sys.argv[4])
in_filenames= sys.argv[5:]
"""

out_type = args.out_type
sort_type = args.sort_type
summary_type = args.summary_type
debug_level = args.debug_level
# use the argument as pattern
bonus_filenames = glob.glob(args.bonus_file[0])
dividend_filenames = glob.glob(args.dividend_file[0])
buyback_filenames = glob.glob(args.buyback_file[0])

# print('bonus_filenames', bonus_filenames)
# print('dividend_filenames', dividend_filenames)

# Error-1, Warn-2, Log-3
companies = []
industries = []
sectors = []
dividend_count = {}
dividend_amount = {}
bonus_share = {}
bonus_count = {}
buyback_share = {}
buyback_count = {}
company_aliases = {}
total_dividend = 0


def load_dividend(row, security_name, purpose):
    try:
        m = re.search("(.*)(Dividend - Rs. -)(.*)", purpose)
        if m.group(2) != "Dividend - Rs. -":
            if debug_level > 1:
                print('no dividend match', row)
            return
        else:
            companies.append(security_name)

        if security_name in dividend_count.keys():
            dividend_count[security_name] += 1
            dividend_amount[security_name] = dividend_amount[security_name] + ' & ' + str(round(float(m.group(3)), 1))
        else:
            dividend_count[security_name] = 1
            dividend_amount[security_name] = str(round(float(m.group(3)), 1))
    except NameError:
        if debug_level > 1:
            print('NameError', row)
    except AttributeError:
        if debug_level > 1:
            print('AttributeError', row)


def load_bonus(row, security_name, purpose):
    try:
        m = re.search("(Bonus issue)(.*)", purpose)
        if m.group(1) != "Bonus issue":
            if debug_level > 1:
                print('no bonus match', row)
            return
        else:
            companies.append(security_name)

        if security_name in bonus_share.keys():
            bonus_count[security_name] += 1
            bonus_share[security_name] = bonus_share[security_name] + ' & ' + m.group(2)
        else:
            bonus_count[security_name] = 1
            bonus_share[security_name] = m.group(2)

    except NameError:
        if debug_level > 1:
            print('NameError', row)
    except AttributeError:
        if debug_level > 1:
            print('AttributeError', row)


def load_buyback(row, security_name, purpose):
    try:
        m = re.search("(Buy Back of Shares)(.*)", purpose)
        if m.group(1) != "Buy Back of Shares":
            if debug_level > 1:
                print('no buyback match', row)
            return
        else:
            companies.append(security_name)

        if security_name in buyback_count.keys():
            buyback_count[security_name] += 1
        else:
            buyback_count[security_name] = 1

    except NameError:
        if debug_level > 1:
            print('NameError', row)
    except AttributeError:
        if debug_level > 1:
            print('AttributeError', row)


def load_row(data_type, row):
    security_code, security_name, company_name, ex_date, purpose, record_date, bc_state_date, bc_end_date, nd_start_date, nd_end_date, actual_payment_date = row

    # company_name = company_name.capitalize()
    # company_name = company_name.strip()
    security_name = security_name.strip()
    if data_type == "d":
        load_dividend(row, security_name, purpose)
    if data_type == "b":
        load_bonus(row, security_name, purpose)
    if data_type == "bb":
        load_buyback(row, security_name, purpose)


def load_data(data_type, in_filenames):
    for in_filename in in_filenames:
        with open(in_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                load_row(data_type, row)


load_data('d', dividend_filenames)
load_data('b', bonus_filenames)
load_data('bb', buyback_filenames)

companies.sort()

if sort_type == "company_name_only":
    for cname in sorted(set(companies)):
        print(cname)

# calculate frequency of occurence of each company
comp_freq = Counter(companies)

if debug_level > 1:
    print(comp_freq)

if sort_type == "sort_frequency_name_only":
    for key, value in sorted(comp_freq.items()):
        print(key)

try:
    if sort_type == "total_count":
        items = comp_freq.items()
        print('security_name, bonus_count, buyback_count, dividend_count, total_count')
    if sort_type == "bonus_count":
        items = bonus_count.items()
        print('security_name, bonus_share, bonus_count')
    if sort_type == "buyback_count":
        items = buyback_count.items()
        print('security_name, buyback_share, buyback_count')
    if sort_type == "dividend_count":
        items = dividend_count.items()
        print('security_name, dividend_amount, dividend_count')

    for key, value in sorted(items, key=itemgetter(1)):
        if key in bonus_share.keys():
            bonus_share_column = bonus_share[key]
        else:
            bonus_share_column = "-"

        if key in bonus_count.keys():
            bonus_count_column = bonus_count[key]
        else:
            bonus_count_column = "-"

        if key in buyback_count.keys():
            buyback_count_column = buyback_count[key]
        else:
            buyback_count_column = "-"

        if key in buyback_share.keys():
            buyback_share_column = buyback_share[key]
        else:
            buyback_share_column = "-"

        if key in dividend_amount.keys():
            dividend_amount_column = dividend_amount[key]
        else:
            dividend_amount_column = "-"

        if key in dividend_count.keys():
            dividend_count_column = dividend_count[key]
        else:
            dividend_count_column = "-"

        if debug_level > 0:
            print(key, bonus_share_column, dividend_amount_column, bonus_count_column, buyback_count_column,
                  dividend_count_column,
                  comp_freq[key])

        if sort_type == "total_count":
            print(key, ',', bonus_count_column, ',', buyback_count_column, ',', dividend_count_column, ',',
                  comp_freq[key])
        if sort_type == "bonus_count":
            print(key, ',', bonus_share_column, ',', bonus_count_column)
        if sort_type == "buyback_count":
            print(key, ',', buyback_share_column, ',', buyback_count_column)
        if sort_type == "dividend_count":
            print(key, ',', dividend_amount_column, ',', dividend_count_column)

except KeyError:
    print('failed key :', key)
