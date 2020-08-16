#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3

import logging

import cutil.cutil

from prettytable import PrettyTable

from database.database import *


class Bhav(Database):
    def __init__(self):
        super(Bhav, self).__init__()
        # isin number
        self.bhav_isin_list = []
        self.bhav_ticker_list = []
        self.bhav_ticker_isin_dict = {}
        self.bhav_ticker_cmp_dict = {}
        self.debug_level = 0
        self.bhav_table_truncate = False
        self.bhav_table_name = "global_bhav"
        self.bhav_table_dict = {
            "bhav_ticker": "text",
            "bhav_price": "float",
            "bhav_isin": "text"
        }

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def bhav_table_reload(self, truncate=False):
        self.bhav_table_truncate = truncate

    def bhav_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                logging.info('ignored empty row %s', row_list)
                return

            comp_rank = row_list[0]
            if comp_rank == 'SYMBOL':
                logging.info('skipped header line %s', row_list)
                return

            symbol_ticker = row_list[0]
            last_price = row_list[1]
            isin_number = row_list[2]

            logging.debug('symbol_ticker : %s', symbol_ticker)
            logging.debug('last_price : %s', last_price)
            logging.debug('isin_number: %s', isin_number)

            self.bhav_ticker_cmp_dict[symbol_ticker] = last_price
            self.bhav_ticker_isin_dict[symbol_ticker] = isin_number

            self.bhav_isin_list.append(isin_number)
            self.bhav_ticker_list.append(symbol_ticker)

        except IndexError:
            logging.error('except %s', row)
        except:
            logging.error('except %s', row)
            traceback.print_exc()

    def bhav_store_data_to_db(self, in_filename):
        table = self.bhav_table_name

        if self.bhav_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_bhav_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.bhav_insert_data(in_filename)
        else:
            logging.info('bhav data already loaded in db %d', row_count)

    def bhav_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        (SYMBOL, SERIES, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, TOTTRDQTY, TOTTRDVAL, TIMESTAMP, TOTALTRADES, ISIN,
         IGNORE) \
            = row_list

        # remove new line character from end
        IGNORE = IGNORE.strip('\n')

        if SYMBOL == 'SYMBOL':
            logging.info('skipped header line %s', row_list)
            logging.info('len row_list %d', len(row_list))
            return

        # skip some rows
        # retail investors series : EQ and BE
        # EQ - intra day trade allowed (normal trading)
        # BE - trade to trade/T-segment : (no intra day squaring allowed : (accept/give delivery)
        if SERIES != 'EQ':
            return
        # remove any un-required stuff
        new_row = (SYMBOL, LAST, ISIN)
        row_bank.append(new_row)

    def bhav_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.bhav_table_name, self.bhav_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.bhav_table_name, self.bhav_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            # insert row
            row_bank = []
            for line in csvfile:
                self.bhav_get_insert_row(line, row_bank)
            print('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def bhav_load_data_from_db(self):
        table = self.bhav_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug('%s', row)
            self.bhav_load_row(row)

    def bhav_dump(self, pretty_dump, out_filename):

        logging.info('output filename %s', out_filename)

        pt = PrettyTable()
        pt.field_names = ["bhav_ticker", "bhav_last", "bhav_isin"]

        fh = open(out_filename, "w")

        for ticker in sorted(self.bhav_ticker_list):
            logging.debug('ticker  ', ticker)
            # create a list
            row_list = [ticker]
            row_list.append(self.bhav_ticker_cmp_dict[ticker])
            row_list.append(self.bhav_ticker_isin_dict[ticker])

            pt.add_row(row_list)

        if pretty_dump:
            fh.write(str(pt))
            fh.close()

    def bhav_export(self, export_to_file, out_filename):

        logging.info('output filename %s', out_filename)

        field_names = ["bhav_ticker", "bhav_last", "bhav_isin"]

        if export_to_file:
            fh = open(out_filename, "w")
            p_hdr = ','.join(field_names)
            p_hdr += '\n'
            fh.write(p_hdr)

        for ticker in sorted(self.bhav_ticker_list):
            logging.debug('ticker  ', ticker)
            # create a list
            row_list = [ticker]
            row_list.append(str(self.bhav_ticker_cmp_dict[ticker]))
            row_list.append(self.bhav_ticker_isin_dict[ticker])

            p_str = ','.join(row_list)
            p_str += '\n'

            if export_to_file:
                fh.write(p_str);

        if export_to_file:
            fh.close()
