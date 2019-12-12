#!/usr/bin/python

import sys
import re
import csv
import traceback

from collections import Counter
from operator import itemgetter

import cutil.cutil

from amfi.amfi import *

class Dividend(Amfi):

    def __init__(self):
        super(Dividend, self).__init__()
        self.multiplier = 0
        self.debug_level = 0
        self.last_row = ""
        self.companies=[]
        self.company_real_name_db=[]
        self.dividend_amount={}
        self.dividend_amount_ym_kv = {}
        self.dividend_cumm_year_kv = {}
        self.dividend_cumm_month_kv = {}
        self.company_aliases={}
        self.company_orig={}
        self.dividend_year_list = []
        self.total_dividend = 0
        # conglomerate name db
        self.cong_name_db=[]
        print('init : Dividend')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def ignore_txn(self, line, txn_remarks):
        # match for search at begining
        # NEFT or RTGS or MMT - Mobile money Transfer
        if re.match('NEFT-|RTGS-|MMT/', txn_remarks):
            if self.debug_level > 2:
                print('NEFT-/RTGS-/MMT skipped' + line)
            return True

        # CASH deposit
        if re.match('BY CASH.*', txn_remarks):
            if self.debug_level > 2:
                print('CASH skipped' + line)
            return True

        # Interest paid - anywhere in string
        if re.search('.*:Int\.Pd:.*', txn_remarks):
            if self.debug_level > 2:
                print('Int.Pd skipped' + line)
            return True

        # APBS / BLPGCM : Aadhaar Payment Bridge System for LPG Subsidy
        if re.match('APBS/.*', txn_remarks):
            if self.debug_level > 2:
                print('APBS skipped' + line)
            return True

        return False

    def normalize_company_name(self, company_name):
        # old orig name
        orig_name = company_name
        # capitalize
        company_name = company_name.capitalize()
        # remove . (TCS.) and hyphen (2017-2018), Lupin$
        company_name = re.sub('\.|-|\$','', company_name)
        # remove 1STINTDIV, 2NDINTDIV, 3RDINTDIV
        company_name = re.sub('1st|2nd|3rd','', company_name)
        # remove FINALDIV etc
        company_name = re.sub('final div|final','', company_name)
        company_name = re.sub('fin div|findiv','', company_name)
        company_name = re.sub('int div|intdiv','', company_name)
        # remove words like DIV, DIVIDEND
        company_name = re.sub('div\.|dividend|div','', company_name)
        # remove any numbers like year 2017, 2018 etc
        company_name = re.sub('\d*','', company_name)
        # remove any characters after (  : colgatepalomolive (india)
        company_name = re.sub('\(.*','', company_name)
        # convert multiple space to single space
        company_name = re.sub(' +', ' ', company_name)
        # remove leading and trailing space
        company_name = company_name.strip()

        company_name = self.resolve_alias(company_name)

        # remove limited, ltd etc
        company_name = re.sub('limited|ltd','', company_name)

        # remove incomplete word
        # remove last word which will be mostly incomplete
        if len(company_name) == 20:
            company_name = company_name.rsplit(' ', 1)[0]

        # remove of india
        company_name = re.sub(' of india','', company_name)
        # remove india
        company_name = re.sub(' india','', company_name)

        company_name = self.resolve_real_company_name_db(company_name)
        self.company_orig[company_name] = orig_name
        if self.debug_level > 1:
            print('orig name', orig_name, 'new name', company_name)
        return company_name

    def load_real_company_name_db():
        comp_name_file_obj = open(comp_filename, 'r')
        for row in comp_name_file_obj:
            name_real = row
            name_real = name_real.strip()
            name_real = name_real.capitalize()
            if debug_level > 2:
                print('real name', name_real)
            self.company_real_name_db.append(name_real)

    def load_conglomerate_name_db():
        cong_name_file_obj = open(cong_filename, 'r')
        for row in cong_name_file_obj:
            name_cong = row
            name_cong = name_cong.strip()
            name_cong = name_cong.capitalize()
            if debug_level > 2:
                print('cong name', name_cong)
            self.cong_name_db.append(name_cong)

    def resolve_alias(self, company_name):
        if company_name in self.company_aliases.keys():
            company_name = self.company_aliases[company_name]
        return company_name

    def resolve_real_company_name_db(self, company_name):
        # avoid tinkering conglomerates with same prefix
        for cong_name in self.cong_name_db:
            if company_name.find(cong_name, 0) >= 0:
                return company_name
        for real_company_name in self.company_real_name_db:
            if company_name.find(real_company_name, 0) >= 0:
                if debug_level > 2:
                    print('replaced from ', company_name, 'to ', real_company_name)
                company_name = real_company_name
                return company_name
        return company_name

    def load_dividend_row(self, line):
        # Replace Limited, with just Limited to avoid split error : ValueError
        line = re.sub(r'Limited,','Limited',line)
        line = re.sub(r'Ltd,','Ltd',line)

        try:
            sno, value_date, txn_date, cheque, txn_remarks, wdraw_amount, deposit_amount = line.split(",")
        except ValueError:
            print('ValueError ', line)

        # avoid cases where txn_remarks itself is double quoted
        txn_remarks = re.sub(r'"','', txn_remarks);

        if txn_remarks == "":
            if line != "":
                if debug_level > 1:
                    print('empty ' + line)
            return

        if self.debug_level > 1:
            print('txn_remarks '+ txn_remarks)
            # pass

        if self.ignore_txn(line, txn_remarks):
            if self.debug_level > 2:
                print('ignored ', txn_remarks)
            return

        if re.match('ACH/.*|CMS/.*', txn_remarks):

            if self.debug_level > 1:
                print(txn_date, txn_remarks, deposit_amount)

            try:
                # dd/mm/yyyy
                txn_date_arr = txn_date.split('/')
                txn_month = txn_date_arr[1].strip()
                # get rid of leading 0 in month number
                txn_month = str(int(txn_month))
                txn_year = txn_date_arr[2].strip()

                remarks_arr = txn_remarks.split('/')
                deposit_way = remarks_arr[0]
                company_name = remarks_arr[1]
                if len(remarks_arr) >= 3:
                    comment_str = remarks_arr[2]
                # ignore rest
            except ValueError:
                print('ValueError ' + txn_remarks)

            # print company_name, deposit_amount
            company_name = self.normalize_company_name(company_name)
            if self.debug_level > 1:
                print('normalized :', company_name)
            ticker = self.amfi_get_ticker_by_name(company_name)
            if self.debug_level > 1:
                print(' ticker :', ticker)
            isin = self.amfi_get_value_by_ticker(ticker, "isin")
            if self.debug_level > 1:
                print(' isin :', isin)
            if ticker != "UNK_TICKER" :
                company_name = ticker

            self.companies.append(company_name)

            if company_name in self.dividend_amount.keys():
                if self.debug_level > 1:
                    print('dividend amount :', self.dividend_amount[company_name])
                    print('deposit amount :', deposit_amount)
                self.dividend_amount[company_name] = int(self.dividend_amount[company_name]) + int(float(deposit_amount))
            else:
                self.dividend_amount[company_name] = int(float(deposit_amount))

            if (txn_year, txn_month) not in self.dividend_amount_ym_kv:
                self.dividend_amount_ym_kv[txn_year, txn_month] = int(float(deposit_amount))

                if txn_year in self.dividend_cumm_year_kv:
                    self.dividend_cumm_year_kv[txn_year] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_year_kv[txn_year] = int(float(deposit_amount))

                if txn_month in self.dividend_cumm_month_kv:
                    self.dividend_cumm_month_kv[txn_month] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_month_kv[txn_month] = int(float(deposit_amount))

                if self.debug_level > 1:
                    print(txn_year, txn_month, 'set div amount : ', int(float(deposit_amount)))
            else:
                self.dividend_amount_ym_kv[txn_year, txn_month] += int(float(deposit_amount))
                if txn_year in self.dividend_cumm_year_kv:
                    self.dividend_cumm_year_kv[txn_year] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_year_kv[txn_year] = int(float(deposit_amount))

                if txn_month in self.dividend_cumm_month_kv:
                    self.dividend_cumm_month_kv[txn_month] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_month_kv[txn_month] = int(float(deposit_amount))

                if self.debug_level > 1:
                    print(txn_year, txn_month, 'added div amount : ', int(float(deposit_amount)))
                    print(txn_year, txn_month, 'accumulated div amount : ',
                          self.dividend_amount_ym_kv[txn_year, txn_month])

            if txn_year not in self.dividend_year_list:
                if self.debug_level > 0:
                    print('added dividend year', txn_year)
                self.dividend_year_list.append(txn_year)

            return

        if self.debug_level > 1:
            print('Unknown skipped' + line)
        return

    def load_dividend_data(self, in_filenames):
        for in_filename in in_filenames:
            if self.debug_level > 1:
                print('div file', in_filename)
            file_obj = open (in_filename, "r")
            for line in file_obj:
                if self.debug_level > 1:
                    print('div line', line)
                self.load_dividend_row(line)
        print('loaded dividend', len (self.dividend_amount))

    def load_aliases_row(self, row):
        try:
            name_alias, ticker = row
        except ValueError:
            print('ValueError ', row)

        name_alias = name_alias.strip().capitalize()
        ticker = ticker.strip().upper()
        if self.debug_level > 2:
            print('alias ', name_alias, 'ticker ', ticker)
        self.company_aliases[name_alias] = ticker

    def load_aliases_data(self, in_filename):
        with open(in_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.load_aliases_row(row)
        print('loaded aliases', len (self.company_aliases))

    def dump_orig(self, out_filename):
        if self.debug_level > 2:
            print(self.company_orig)
        lines = []
        fh = open(out_filename, "w")
        for comp_name in self.company_orig.keys():
            p_str = comp_name
            p_str += ','
            p_str += self.company_orig[comp_name]
            p_str += '\n'
            lines.append(p_str)
        fh.writelines(lines)
        return

    # sort_type
    def print_phase0(self, out_filename, sort_type):
        # sort companies
        self.companies.sort()

        total_dividend = 0
        for value in self.dividend_amount.values() :
            total_dividend += value

        # calculate frequency of occurence of each company
        comp_freq = Counter(self.companies)

        if self.debug_level > 1:
            print(comp_freq)

        lines = []
        fh = open(out_filename, "w")

        if sort_type == "name_only":
            for key, value in sorted(comp_freq.items()):
                p_str = key
                p_str += '\n'
                lines.append(p_str)
        if sort_type == "monthly_dividend":
            year_iter = 0
            for txn_year in sorted(self.dividend_year_list):
                year_iter += 1
                if len(self.dividend_year_list) == 2:
                    if year_iter == 1:
                        month_start = 4
                        # use 13 to include month till 12
                        month_end = 13
                    else:
                        month_start = 1
                        # use 4 to include till 3
                        month_end = 4
                elif len(self.dividend_year_list) == 1:
                    # no new entries from new financial year yet
                    month_start = 4
                    # use 13 to include month till 12
                    month_end = 13
                else:
                    # all
                    month_start = 1
                    # use 13 to include month till 12
                    month_end = 13
                # april to march
                # header
                if not (len(self.dividend_year_list) == 2 and year_iter == 2):
                    p_str = 'year'
                else:
                    p_str = ''

                if year_iter == 1:
                    for txn_month_int in range(month_start, month_end):
                        # txn_month = str(txn_month_int)
                        txn_month_abre = datetime.date(1900, txn_month_int, 1).strftime('%b')
                        p_str += ',' + str(txn_month_abre)

                    if len(self.dividend_year_list) == 2:
                        month_start_2 = 1
                        # use 4 to include till 3
                        month_end_2 = 4

                        for txn_month_int in range(month_start_2, month_end_2):
                            # txn_month = str(txn_month_int)
                            txn_month_abre = datetime.date(1900, txn_month_int, 1).strftime('%b')
                            p_str += ',' + str(txn_month_abre)

                    # all data
                    if len(self.dividend_year_list) > 2:
                        p_str += ',' + 'sum'
                    p_str += '\n'
                    lines.append(p_str)

                # actual data
                if not (len(self.dividend_year_list) == 2 and year_iter == 2):
                    # display FY
                    if len(self.dividend_year_list) == 2 and year_iter == 1:
                        next_year = int(txn_year) + 1
                        p_str = 'FY-' + str(txn_year) + '/' + str(next_year)
                    else:
                        p_str = str(txn_year)
                else:
                    p_str = ''

                for txn_month_int in range(month_start, month_end):
                    txn_month = str(txn_month_int)
                    if (txn_year, txn_month) in self.dividend_amount_ym_kv:
                        p_str += ',' + str(self.dividend_amount_ym_kv[str(txn_year), str(txn_month)])
                    else:
                        p_str += ',' + '0'

                if len(self.dividend_year_list) == 2:
                    if year_iter == 2:
                        p_str += '\n'
                else:
                    # include cumulative data
                    if len(self.dividend_year_list) > 2:
                        p_str += ',' + str(self.dividend_cumm_year_kv[txn_year])
                    p_str += '\n'
                lines.append(p_str)

                if len(self.dividend_year_list) > 2 and year_iter == len(self.dividend_year_list):
                    p_str = 'sum'
                    for txn_month_int in range(month_start, month_end):
                        txn_month = str(txn_month_int)
                        p_str += ',' + str(self.dividend_cumm_month_kv[txn_month])
                    # for the last sum column
                    p_str += ',' + '-' + '\n'
                    lines.append(p_str)

        elif sort_type == "sort_name" :
            for key, value in sorted(comp_freq.items()):
                p_str = key
                p_str += ','
                p_str += str(value)
                p_str += ','
                p_str += str(self.dividend_amount[key])
                p_str += '\n'
                lines.append(p_str)
        elif sort_type == "sort_frequency" :
            for key, value in sorted(comp_freq.items(), key=itemgetter(1)):
                p_str = key
                p_str += ','
                p_str += str(value)
                p_str += ','
                p_str += str(self.dividend_amount[key])
                p_str += '\n'
                lines.append(p_str)
        elif sort_type == "sort_amount":
            for key, value in sorted(self.dividend_amount.items(), key=itemgetter(1)) :
                p_str = key
                p_str += ','
                p_str += str(comp_freq[key])
                p_str += ','
                p_str += str(self.dividend_amount[key])
                p_str += '\n'
                lines.append(p_str)
        fh.writelines(lines)
        return

    # name_only
    def print_phase1(self, out_filename):
        self.print_phase0(out_filename, "name_only")

    # sort_name
    def print_phase2(self, out_filename):
        self.print_phase0(out_filename, "sort_name")

    # sort_frequency
    def print_phase3(self, out_filename):
        self.print_phase0(out_filename, "sort_frequency")

    # sort_amount
    def print_phase4(self, out_filename):
        self.print_phase0(out_filename, "sort_amount")

    # monthly dividend
    def print_phase5(self, out_filename):
        self.print_phase0(out_filename, "monthly_dividend")
