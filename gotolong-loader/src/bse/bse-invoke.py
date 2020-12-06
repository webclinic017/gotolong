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

from datetime import date

import glob

import traceback

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
parser.add_argument('--out_file', dest='out_file', help='out file')

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
output_filename = args.out_file

print('out file :', output_filename)

# print('bonus_filenames', bonus_filenames)
# print('dividend_filenames', dividend_filenames)

# Error-1, Warn-2, Log-3
current_date = date.today()
current_year = current_date.year

corp_act_stock_list = []
corp_act_dividend_stock_year_dict = {}
corp_act_bonus_stock_year_dict = {}
corp_act_buyback_stock_year_dict = {}

corp_act_year_list = []

total_giveback_score = {}
bonus_score = {}
buyback_score = {}
dividend_score = {}


def bse_load_any(row, security_name, ex_date, purpose):
    try:
        if purpose == '-' or purpose == 'Purpose':
            return

        if ex_date != 'Ex Date':
            # sometime the space is separator and sometime hyphen is separator
            if re.search('-', ex_date):
                split_char = "-"
            else:
                split_char = " "
            date_arr = ex_date.split(split_char)
            if debug_level > 2:
                print('date: ', date_arr)
            current_year = int(date_arr[2])
            # note: sometime date is stored as 17 and sometime as 2017
            # to fix the year.
            if current_year >= 2000:
                current_year = current_year - 2000
            if debug_level > 2:
                print('year : ', current_year)

            if security_name not in corp_act_stock_list:
                corp_act_stock_list.append(security_name)
            if current_year not in corp_act_year_list:
                corp_act_year_list.append(current_year)

            if re.search('Bonus', purpose):
                if (security_name, current_year) not in corp_act_bonus_stock_year_dict:
                    corp_act_bonus_stock_year_dict[security_name, current_year] = 1
            elif re.search('Buy Back', purpose):
                if (security_name, current_year) not in corp_act_buyback_stock_year_dict:
                    corp_act_buyback_stock_year_dict[security_name, current_year] = 1
            elif re.search('Dividend', purpose):
                if (security_name, current_year) not in corp_act_dividend_stock_year_dict:
                    corp_act_dividend_stock_year_dict[security_name, current_year] = 1
            else:
                print('wrong purpose', purpose)

    except IndexError:
        if debug_level > 1:
            print('IndexError', row)
        traceback.print_exc()
        traceback.print_exc()
    except NameError:
        if debug_level > 1:
            print('NameError', row)
        traceback.print_exc()
    except AttributeError:
        if debug_level > 1:
            print('AttributeError', row)
        traceback.print_exc()



def bse_load_row(data_type, row):
    security_code, security_name, company_name, ex_date, purpose, record_date, bc_state_date, bc_end_date, nd_start_date, nd_end_date, actual_payment_date = row

    # company_name = company_name.capitalize()
    # company_name = company_name.strip()
    security_name = security_name.strip()
    purpose = purpose.strip()
    ex_date = ex_date.strip()

    bse_load_any(row, security_name, ex_date, purpose)


def bse_load_data(data_type, in_filenames):
    for in_filename in in_filenames:
        with open(in_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                bse_load_row(data_type, row)


bse_load_data('d', dividend_filenames)
bse_load_data('b', bonus_filenames)
bse_load_data('bb', buyback_filenames)
# stock split is not giving back
# bse_load_data('ss', split_filenames)

if sort_type == "corpact":

    print('year list: ', sorted(set(corp_act_year_list)))

    for security_name in sorted(set(corp_act_stock_list)):
        buyback_found = 0
        bonus_found = 0
        dividend_found = 0

        for current_year in sorted(set(corp_act_year_list), key=int):
            try:
                if (security_name, current_year) in corp_act_buyback_stock_year_dict:
                    buyback_found += 1
                if (security_name, current_year) in corp_act_bonus_stock_year_dict:
                    bonus_found += 1
                if (security_name, current_year) in corp_act_dividend_stock_year_dict:
                    dividend_found += 1
                    if debug_level > 2:
                        print(security_name, current_year)

            except KeyError:
                print('KeyError failed lookup :', security_name, current_year)
        # do not include stock split as that doesn't mean giving back
        total_give_back = buyback_found + bonus_found + dividend_found
        bonus_score[security_name] = bonus_found
        buyback_score[security_name] = buyback_found
        dividend_score[security_name] = dividend_found
        total_giveback_score[security_name] = total_give_back

    fh = open(output_filename, "w")
    p_str = 'security_name, total_score, bonus_score, buyback_score, dividend_score\n'
    fh.write(p_str)

    try:
        for security_name in sorted(total_giveback_score, key=lambda i: int(total_giveback_score[i]), reverse=True):
            p_str = security_name
            p_str += ','
            p_str += str(total_giveback_score[security_name])
            p_str += ','
            p_str += str(bonus_score[security_name])
            p_str += ','
            p_str += str(buyback_score[security_name])
            p_str += ','
            p_str += str(dividend_score[security_name])
            p_str += '\n'
            fh.write(p_str)
    except KeyError:
        print('KeyError failed lookup 2:', security_name, current_year)
    fh.close()
