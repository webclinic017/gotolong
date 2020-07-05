#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3

import cutil.cutil

from database.database import *

class Amfi(Database):
    def __init__(self):
        super(Amfi, self).__init__()
        # isin number
        self.amfi_isin_list = []
        self.amfi_ticker_list = []
        self.amfi_captype_list = []
        # serial number
        self.amfi_cname = {}
        self.amfi_mcap = {}
        self.amfi_rank = {}
        self.amfi_captype = {}
        self.amfi_ticker_isin_dict = {}
        self.amfi_isin_ticker_dict = {}
        self.debug_level = 0
        self.amfi_table_truncate = False
        self.amfi_table_name = "global_amfi"
        self.amfi_table_dict = {
            "comp_rank": "int",
            "comp_name": "text",
            "comp_isin": "text",
            "bse_symbol": "text",
            "nse_symbol": "text",
            "avg_mcap": "text",
            "cap_type": "text",
        }

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def amfi_table_reload(self, truncate=False):
        self.amfi_table_truncate = truncate

    def amfi_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            comp_rank = row_list[0]
            if comp_rank == 'Sr. No.' or comp_rank == "sr_no":
                if self.debug_level > 0:
                    print('skipped header line', row_list)
                return

            # mysql - automatically number
            if self.config_db_type != 'mariadb':
                comp_rank = cutil.cutil.get_number(comp_rank)

            comp_name = row_list[1]
            isin_number = row_list[2]
            bse_ticker = row_list[3].upper().strip()
            nse_ticker = row_list[4]
            if self.config_db_type == 'mariadb':
                avg_mcap = row_list[5]
            else:
                avg_mcap = cutil.cutil.get_number(row_list[5])
            captype = row_list[6].strip()

            comp_name = cutil.cutil.normalize_comp_name(comp_name)

            if self.debug_level > 1:
                print('comp_rank : ', comp_rank)
                print('isin_number: ', isin_number)
                print('bse_ticker : ', bse_ticker)
                print('nse_ticker : ', nse_ticker)
                print('avg_mcap : ', avg_mcap )
                print('captype : ', captype )
                print('comp_name : ', comp_name)

            if nse_ticker == '':
                if bse_ticker != '':
                    self.amfi_rank[bse_ticker] = comp_rank
                    self.amfi_ticker_isin_dict[bse_ticker] = isin_number
                    self.amfi_isin_ticker_dict[isin_number] = nse_ticker
                    self.amfi_cname[bse_ticker] = comp_name
                    self.amfi_mcap[bse_ticker] = avg_mcap
                    self.amfi_captype[bse_ticker] = captype
                    self.amfi_isin_list.append(isin_number)
                    self.amfi_ticker_list.append(bse_ticker)
            else:
                self.amfi_rank[nse_ticker] = comp_rank
                self.amfi_ticker_isin_dict[nse_ticker] = isin_number
                self.amfi_isin_ticker_dict[isin_number] = nse_ticker
                self.amfi_cname[nse_ticker] = comp_name
                self.amfi_mcap[nse_ticker] = avg_mcap
                self.amfi_captype[nse_ticker] = captype
                self.amfi_isin_list.append(isin_number)
                self.amfi_ticker_list.append(nse_ticker)

            if captype not in self.amfi_captype_list:
                self.amfi_captype_list.append(captype)

            if self.debug_level > 1:
                print('comp_name : ', comp_name , '\n')
                print('isin_number: ', isin_number, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def amfi_load_data(self, in_filename):
        table = self.amfi_table_name

        if self.amfi_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_amfi_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.amfi_insert_data(in_filename)
        else:
            print('amfi data already loaded in db', row_count)
        print('display db data')
        self.amfi_load_db()

    def amfi_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')



        (comp_rank, comp_name, comp_isin, bse_symbol, nse_symbol, avg_mcap, cap_type) = row_list

        # remove new line character from end
        cap_type = cap_type.strip('\n')

        if comp_rank == 'Sr. No.' or comp_rank == "sr_no":
            if self.debug_level > 0:
                print('skipped header line', row_list)
                print('len row_list', len(row_list))
            return

        # remove any un-required stuff
        new_row = (comp_rank, comp_name, comp_isin, bse_symbol, nse_symbol, avg_mcap, cap_type)
        row_bank.append(new_row)

    def amfi_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.amfi_table_name, self.amfi_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.amfi_table_name, self.amfi_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            # insert row
            row_bank = []
            for line in csvfile:
                self.amfi_get_insert_row(line, row_bank)
            print('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def amfi_load_db(self):
        table = self.amfi_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1 :
                print(row)
            self.amfi_load_row(row)

    def amfi_dump_phase1(self, out_filename):
        if self.debug_level > 0:
            print('output filename ', out_filename)
        fh = open(out_filename, "w")
        fh.write('amfi_rank, amfi_cname, amfi_isin, amfi_ticker, amfi_mcap, amfi_captype\n')
        for ticker in sorted(self.amfi_rank, key=self.amfi_rank.__getitem__):
            if self.debug_level > 1:
                print('ticker  ', ticker)
            p_str = str(self.amfi_rank[ticker])
            p_str += ', '
            p_str += self.amfi_cname[ticker]
            p_str += ', '
            p_str += self.amfi_ticker_isin_dict[ticker]
            p_str += ', '
            p_str += ticker
            p_str += ', '
            p_str += str(self.amfi_mcap[ticker])
            p_str += ', '
            p_str += self.amfi_captype[ticker]
            p_str += '\n'
            fh.write(p_str);
        fh.close()

    def amfi_get_ticker_by_name(self, req_name):
        req_name = re.sub('\s+', ' ', req_name).strip()
        for amfi_ticker in sorted(self.amfi_cname):
            # try to find a matching company
            comp_name = self.amfi_cname[amfi_ticker]
            comp_name = comp_name.strip()
            if re.match(req_name, comp_name) or req_name.upper() == amfi_ticker:
                if self.debug_level > 1:
                    print('found match : name : ', req_name)
                return amfi_ticker
        if self.debug_level > 1:
            print('amfi : comp not found : req_name :',req_name,':')
        return ''

    def amfi_get_value_by_isin(self, isin, value_name):
        # return ticker
        if value_name == "ticker":
            return self.amfi_get_ticker_by_isin(isin)
        try:
            ticker = self.amfi_isin_ticker_dict[isin]
            if ticker:
                self.amfi_get_value_by_ticker(self, isin, value_name)
        except KeyError:
            print('KeyError ', isin)
            traceback.print_exc()
        return 'UNK_COMP_2'

    def amfi_get_value_by_ticker(self, ticker, value_name):
        try:
            if ticker:
                if value_name == "cname":
                    return self.amfi_cname[ticker]
                if value_name == "mcap":
                    return self.amfi_mcap[ticker]
                if value_name == "rank":
                    return self.amfi_rank[ticker]
                if value_name == "captype":
                    return self.amfi_captype[ticker]
                if value_name == "isin":
                    return self.amfi_get_isin_by_ticker(ticker)
        except KeyError:
            print('KeyError ', ticker)
            traceback.print_exc()
        except:
            print('Except ', ticker)
            traceback.print_exc()
        if value_name == "mcap" or value_name == "rank":
            return 0
        else:
            return 'UNK_COMP_E'

    def amfi_get_ticker_by_isin(self, amfi_isin):
        if amfi_isin in self.amfi_isin_list:
            return self.amfi_isin_ticker_dict[amfi_isin]
        return 'UNK_TICKER'

    def amfi_get_isin_by_ticker(self, ticker):
        try:
            amfi_isin = self.amfi_ticker_isin_dict[ticker]
            if amfi_isin:
                return amfi_isin
        except KeyError:
            print('KeyError ', ticker)
            traceback.print_exc()
        return 'UNK_ISIN'
