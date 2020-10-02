#!/usr/bin/python

import sys
import re
import csv
import traceback

from collections import Counter
from operator import itemgetter

import cutil.cutil

from amfi.amfi import *
from nach.nach import *

import calendar


class Dividend(Amfi, Nach):

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
        self.dividend_cumm_comp_month_kv = {}
        self.dividend_cumm_comp_kv = {}
        self.company_orig={}
        self.company_name_pre_alias = {}
        self.add_nach_ticker = {}
        self.dividend_year_list = []
        self.total_dividend = 0
        self.dividend_records = []
        self.dividend_abbr_to_num_dict = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        self.dividend_table_truncate = False
        self.dividend_table_name = "user_dividend"
        # do not add 'id' here as that is automatically auto-incremented.
        self.dividend_table_dict = {
            "div_date": "Date",
            "remarks": "text",
            "amount": "text",
            "ticker": "text",
            "isin": "text"
        }

        # conglomerate name db
        self.cong_name_db=[]
        print('init : Dividend')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def dividend_table_reload(self, truncate=False):
        self.dividend_table_truncate = truncate

    def dividend_load_row(self, row):
        row_list = row
        self.dividend_records.append(row_list)

        dividend_date = row_list[0]
        dividend_remarks = row_list[1]
        dividend_amount = row_list[2]
        dividend_comp_name = row_list[3]
        dividend_ticker = row_list[4]
        dividend_isin = row_list[5]

    def dividend_txn_ignore(self, line, txn_remarks):
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

    def dividend_company_name_normalize(self, company_name):
        # old orig name
        orig_name = company_name

        company_name = company_name.upper()

        # capitalize
        company_name = company_name.capitalize()

        # remove . (TCS.) and hyphen (2017-2018), Lupin$
        company_name = re.sub('\.|-|\$','', company_name)
        # remove 1STINTDIV, 2NDINTDIV, 3RDINTDIV
        company_name = re.sub('1st|2nd|3rd', '', company_name, flags=re.IGNORECASE)
        # remove FINALDIV etc
        company_name = re.sub('final div|final', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub('fin div|findiv', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub('int div|intdiv', '', company_name, flags=re.IGNORECASE)
        # remove words like DIV, DIVIDEND
        company_name = re.sub('div\.|dividend|div', '', company_name, flags=re.IGNORECASE)

        # remove payout by
        company_name = re.sub('Payout by', '', company_name)
        # remove any numbers like year 2017, 2018 etc
        company_name = re.sub('\d*','', company_name)
        # remove any characters after (  : colgatepalomolive (india)
        company_name = re.sub('\(.*','', company_name)
        # convert multiple space to single space
        company_name = re.sub(' +', ' ', company_name)
        # remove leading and trailing space
        company_name = company_name.strip()

        # remove of india
        company_name = re.sub(' of ', ' ', company_name, flags=re.IGNORECASE)
        # remove india - from end
        company_name = re.sub(' india$', ' ', company_name, flags=re.IGNORECASE)
        # remove india in the middle
        company_name = re.sub(' india ', ' ', company_name, flags=re.IGNORECASE)

        # special payment
        company_name = re.sub(' SP$', '', company_name, flags=re.IGNORECASE)

        # INTERIM
        company_name = re.sub(' INTERIM$', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub(' INT$', '', company_name, flags=re.IGNORECASE)

        company_name = re.sub(' FY$', '', company_name, flags=re.IGNORECASE)

        # removed LIMITED, LTD, LIMITE etc
        company_name = re.sub(' LIMITED$| LTD$| LIMITE$', '', company_name, flags=re.IGNORECASE)

        # LIMIT$, LIMI$, LIM$, LI$, L$
        company_name = re.sub(' LIMIT$| LIMI$| LIM$| LI$| L$', '', company_name, flags=re.IGNORECASE)

        # cor$, corp.*$
        company_name = re.sub(' COR$| CORP.*$', '', company_name, flags=re.IGNORECASE)

        # in.*$ industries
        company_name = re.sub(' IN.*$', '', company_name, flags=re.IGNORECASE)

        # remove &
        # company_name = re.sub('&', '', company_name, flags=re.IGNORECASE)

        name_before_resolve_alias = company_name
        company_name = self.dividend_resolve_alias(company_name)

        self.company_orig[company_name] = orig_name
        self.company_name_pre_alias[company_name] = name_before_resolve_alias

        if self.debug_level > 1:
            print('orig name', orig_name, 'new name', company_name)
        return company_name

    def dividend_resolve_alias(self, company_name):
        if company_name in self.nach_aliases.keys():
            company_name = self.nach_aliases[company_name]
        return company_name

    def dividend_get_insert_row(self, line, row_bank):
        # Replace Limited, with just Limited to avoid split error : ValueError
        line = re.sub(r'Limited,','Limited',line)
        line = re.sub(r'Ltd,','Ltd',line)

        try:
            txn_date, txn_remarks, deposit_amount = line.split(",")
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

        if self.dividend_txn_ignore(line, txn_remarks):
            if self.debug_level > 2:
                print('ignored ', txn_remarks)
            return

        if re.match('ACH/.*|CMS/.*', txn_remarks):

            if self.debug_level > 1:
                print(txn_date, txn_remarks, deposit_amount)

            try:
                # dd/mm/yyyy
                txn_date_arr = txn_date.split('/')
                txn_day = txn_date_arr[0].strip()
                txn_month = txn_date_arr[1].strip()
                txn_year = txn_date_arr[2].strip()
                if txn_month.isdigit():
                    # get rid of leading 0 in month number
                    txn_month = str(int(txn_month))
                else:
                    # month name to number
                    txn_month = self.dividend_abbr_to_num_dict[txn_month]

                remarks_arr = txn_remarks.split('/')
                deposit_way = remarks_arr[0]
                company_name = remarks_arr[1]
                if len(remarks_arr) >= 3:
                    comment_str = remarks_arr[2]

                div_date_iso = txn_year + "-" + txn_month + "-" + txn_day
                # ignore rest
            except ValueError:
                print('ValueError ' + txn_remarks)

            # print company_name, deposit_amount
            company_name = self.dividend_company_name_normalize(company_name)
            if self.debug_level > 1:
                print('normalized :', company_name)
            ticker = self.amfi_get_ticker_by_name(company_name)
            if self.debug_level > 1:
                print(' ticker :', ticker)
            isin = self.amfi_get_value_by_ticker(ticker, "isin")
            if self.debug_level > 1:
                print(' isin :', isin)
            if ticker != '' and ticker != "UNK_TICKER":
                if self.debug_level > 1:
                    print('company is ticker', ticker)
                company_name = ticker
            else:
                pre_alias_name = self.company_name_pre_alias[company_name]
                if pre_alias_name in self.add_nach_ticker:
                    pass
                else:
                    self.add_nach_ticker[pre_alias_name] = 'yes'
                    if self.debug_level > 1:
                        print('add nach ticker alias for', company_name, ':', pre_alias_name, ':')

            new_row = (div_date_iso, txn_remarks, deposit_amount, ticker, isin)
            row_bank.append(new_row)

            if self.debug_level > 1:
                print(company_name, 'from', txn_remarks)

            if company_name not in self.companies:
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

                if (company_name, txn_month) in self.dividend_cumm_comp_month_kv:
                    self.dividend_cumm_comp_month_kv[company_name, txn_month] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_comp_month_kv[company_name, txn_month] = int(float(deposit_amount))

                if company_name in self.dividend_cumm_comp_kv:
                    self.dividend_cumm_comp_kv[company_name] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_comp_kv[company_name] = int(float(deposit_amount))

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

                if (company_name, txn_month) in self.dividend_cumm_comp_month_kv:
                    self.dividend_cumm_comp_month_kv[company_name, txn_month] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_comp_month_kv[company_name, txn_month] = int(float(deposit_amount))

                if company_name in self.dividend_cumm_comp_kv:
                    self.dividend_cumm_comp_kv[company_name] += int(float(deposit_amount))
                else:
                    self.dividend_cumm_comp_kv[company_name] = int(float(deposit_amount))

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

    def dividend_insert_data_core(self, in_filenames):
        for in_filename in in_filenames:
            if self.debug_level > 1:
                print('div file', in_filename)
            file_obj = open (in_filename, "r")
            for line in file_obj:
                if self.debug_level > 1:
                    print('div line', line)
                self.dividend_get_insert_row(line)
        print('loaded dividend', len (self.dividend_amount))



    def dividend_load_data(self, in_filenames):
        table = self.dividend_table_name
        if self.dividend_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.dividend_insert_data(in_filenames)
        else:
            print('dividend data already loaded in db', row_count)
        print('display db data')
        self.dividend_load_db()

    def dividend_insert_data(self, in_filenames):

        create_sql = cutil.cutil.get_create_sql(self.dividend_table_name, self.dividend_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.dividend_table_name, self.dividend_table_dict)

        if self.debug_level > 0:
            print(create_sql)

        cursor = self.db_conn.cursor()

        for in_filename in in_filenames:
            if self.debug_level > 1:
                print('div file', in_filename)

            with open(in_filename, 'rt') as csvfile:
                # future
                # csv_reader = csv.reader(csvfile)
                row_bank = []
                for line in csvfile:
                    self.dividend_get_insert_row(line, row_bank)
                print('loaded entries', len(row_bank), 'from', in_filename)
                # insert row
                cursor.executemany(insert_sql, row_bank)
        # commit db changes
        self.db_conn.commit()

    def dividend_load_db(self):
        table = self.dividend_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.dividend_load_row(row)

    def dividend_dump_orig(self, out_filename):
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
    def dividend_print_phase0(self, out_filename, sort_type):
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
        elif sort_type == "monthly_dividend":
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
                        p_str += ',' + 'Total'
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
                    p_str = 'Total'
                    for txn_month_int in range(month_start, month_end):
                        txn_month = str(txn_month_int)
                        p_str += ',' + str(self.dividend_cumm_month_kv[txn_month])
                    # for the last sum column
                    p_str += ',' + '-' + '\n'
                    lines.append(p_str)

        elif sort_type == "comp_monthly_dividend":

            # all
            month_start = 1
            # use 13 to include month till 12
            month_end = 13

            # header
            p_str = 'comp_name'
            for txn_month_int in range(month_start, month_end):
                # txn_month = str(txn_month_int)
                txn_month_abre = datetime.date(1900, txn_month_int, 1).strftime('%b')
                p_str += ',' + str(txn_month_abre)

            # all data
            p_str += ',' + 'Total'
            p_str += '\n'
            lines.append(p_str)

            comp_iter = 0
            for comp_name in sorted(self.companies):
                comp_iter += 1
                p_str = comp_name
                for txn_month_int in range(month_start, month_end):
                    txn_month = str(txn_month_int)
                    if (comp_name, txn_month) in self.dividend_cumm_comp_month_kv:
                        p_str += ',' + str(self.dividend_cumm_comp_month_kv[comp_name, str(txn_month)])
                    else:
                        # use hyphen instead of 0 to easily identify other numbers
                        p_str += ',' + '-'

                # include cumulative data
                p_str += ',' + str(self.dividend_cumm_comp_kv[comp_name])
                p_str += '\n'
                lines.append(p_str)

                if len(self.companies) == comp_iter:
                    p_str = 'Total'
                    for txn_month_int in range(month_start, month_end):
                        txn_month = str(txn_month_int)
                        if txn_month in self.dividend_cumm_month_kv:
                            p_str += ',' + str(self.dividend_cumm_month_kv[txn_month])
                        else:
                            # use hyphen instead of 0 to easily identify other numbers
                            p_str += ',' + '-'
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

    def dividend_print_missing_nach_alises(self, out_filename):
        lines = []
        fh = open(out_filename, "w")
        for comp_name in sorted(self.add_nach_ticker.keys()):
            p_str = comp_name
            p_str += '\n'
            lines.append(p_str)
        fh.writelines(lines)
        return

    # name_only
    def dividend_print_phase1(self, out_filename):
        self.dividend_print_phase0(out_filename, "name_only")

    # sort_name
    def dividend_print_phase2(self, out_filename):
        self.dividend_print_phase0(out_filename, "sort_name")

    # sort_frequency
    def dividend_print_phase3(self, out_filename):
        self.dividend_print_phase0(out_filename, "sort_frequency")

    # sort_amount
    def dividend_print_phase4(self, out_filename):
        self.dividend_print_phase0(out_filename, "sort_amount")

    # monthly dividend
    def dividend_print_phase5(self, out_filename):
        self.dividend_print_phase0(out_filename, "monthly_dividend")

    # comp monthly dividend
    def dividend_print_phase6(self, out_filename):
        self.dividend_print_phase0(out_filename, "comp_monthly_dividend")

    # missing nach ticker aliases
    def dividend_print_phase7(self, out_filename):
        self.dividend_print_missing_nach_alises(out_filename)
