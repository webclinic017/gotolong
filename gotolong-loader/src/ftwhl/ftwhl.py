#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3
import math

import argparse

import logging

import cutil.cutil

from prettytable import PrettyTable

from database.database import *


class Ftwhl(Database):
    def __init__(self):
        super(Ftwhl, self).__init__()
        # isin number
        self.ftwhl_ticker_list = []
        self.ftwhl_ticker_high_dict = {}
        self.ftwhl_ticker_low_dict = {}
        self.ftwhl_ticker_high_dt_dict = {}
        self.ftwhl_ticker_low_dt_dict = {}
        self.debug_level = 0
        self.ftwhl_table_truncate = False
        self.ftwhl_table_name = "global_ftwhl"
        self.ftwhl_table_dict = {
            "ftwhl_ticker": "text",
            "ftwhl_high": "float",
            "ftwhl_high_dt": "text",
            "ftwhl_low": "float",
            "ftwhl_low_dt": "text"
        }

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def ftwhl_table_reload(self, truncate=False):
        self.ftwhl_table_truncate = truncate

    def ftwhl_load_row(self, row):
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
            high_price = row_list[1]
            high_price_dt = row_list[2]
            low_price = row_list[3]
            low_price_dt = row_list[4]

            logging.debug('symbol_ticker : %s', symbol_ticker)
            logging.debug('high_price : %s', high_price)
            logging.debug('high_price_dt: %s', high_price_dt)
            logging.debug('low_price : %s', low_price)
            logging.debug('low_price_dt: %s', low_price_dt)

            self.ftwhl_ticker_high_dict[symbol_ticker] = high_price
            self.ftwhl_ticker_low_dict[symbol_ticker] = low_price

            self.ftwhl_ticker_high_dt_dict[symbol_ticker] = high_price_dt
            self.ftwhl_ticker_low_dt_dict[symbol_ticker] = low_price_dt

            self.ftwhl_ticker_list.append(symbol_ticker)

        except IndexError:
            logging.error('except %s', row)
        except:
            logging.error('except %s', row)
            traceback.print_exc()

    def ftwhl_store_data_to_db(self, in_filename):
        table = self.ftwhl_table_name

        if self.ftwhl_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_ftwhl_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.ftwhl_insert_data(in_filename)
        else:
            logging.info('ftwhl data already loaded in db %d', row_count)

    def ftwhl_get_insert_row(self, line, row_bank):

        # remove all double quotes
        line = line.replace('"', '')

        # split on comma
        row_list = line.split(',')

        # how to skip first two rows that doesn't match this

        try:

            (SYMBOL, SERIES, high_52, high_52_dt, low_52, low_52_dt) = row_list

            # remove new line character from end
            low_52_dt = low_52_dt.strip('\n')

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
            if math.isnan(float(high_52)):
                high_52 = '0'
                logging.info('high_52 changed to 0 for %s', SYMBOL)
            if math.isnan(float(low_52)):
                low_52 = '0'
                logging.info('low_52 changed to 0 for %s', SYMBOL)

            new_row = (SYMBOL, high_52, high_52_dt, low_52, low_52_dt)
            row_bank.append(new_row)

        except ValueError:
            logging.error('except %s: skipped this row', row_list)

    def ftwhl_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.ftwhl_table_name, self.ftwhl_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.ftwhl_table_name, self.ftwhl_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            # insert row
            row_bank = []
            for line in csvfile:
                self.ftwhl_get_insert_row(line, row_bank)
            print('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def ftwhl_load_data_from_db(self):
        table = self.ftwhl_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug('%s', row)
            self.ftwhl_load_row(row)

    def ftwhl_dump(self, pretty_dump, out_filename):

        logging.info('output filename %s', out_filename)

        pt = PrettyTable()
        pt.field_names = ["ftwhl_ticker", "ftwhl_high", "ftwhl_high_dt", "ftwhl_low", "ftwhl_low_dt"]

        fh = open(out_filename, "w")

        for ticker in sorted(self.ftwhl_ticker_list):
            logging.debug('ticker  ', ticker)
            # create a list
            row_list = [ticker]
            row_list.append(self.ftwhl_ticker_high_dict[ticker])
            row_list.append(self.ftwhl_ticker_high_dt_dict[ticker])
            row_list.append(self.ftwhl_ticker_low_dict[ticker])
            row_list.append(self.ftwhl_ticker_low_dt_dict[ticker])
            pt.add_row(row_list)

        if pretty_dump:
            fh.write(str(pt))
            fh.close()

    def ftwhl_export(self, export_to_file, out_filename):

        logging.info('output filename %s', out_filename)

        field_names = ["ftwhl_ticker", "ftwhl_high", "ftwhl_high_dt", "ftwhl_low", "ftwhl_low_dt"]

        if export_to_file:
            fh = open(out_filename, "w")
            p_hdr = ','.join(field_names)
            p_hdr += '\n'
            fh.write(p_hdr)

        for ticker in sorted(self.ftwhl_ticker_list):
            logging.debug('ticker  ', ticker)
            # create a list
            row_list = [ticker]
            row_list.append(str(self.ftwhl_ticker_high_dict[ticker]))
            row_list.append(self.ftwhl_ticker_high_dt_dict[ticker])
            row_list.append(str(self.ftwhl_ticker_low_dict[ticker]))
            row_list.append(self.ftwhl_ticker_low_dt_dict[ticker])

            p_str = ','.join(row_list)
            p_str += '\n'

            if export_to_file:
                fh.write(p_str);

        if export_to_file:
            fh.close()


def main():
    print('in main')

    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int,
                        choices=[0, 1, 2, 3])
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
        print("usage: " + program_name + " <debug_level : 1-4> <ftwhl.csv> ... ")
        sys.exit(1)

    print('args :', len(sys.argv))

    ftwhl = Ftwhl()

    ftwhl.set_log_level(log_level)

    if truncate_table:
        ftwhl.ftwhl_table_reload(truncate_table)

    if save_to_db:
        ftwhl.ftwhl_store_data_to_db(in_filename_phase[0])

    ftwhl.ftwhl_load_data_from_db()

    ftwhl.ftwhl_export(export_to_file, out_filename_phase[0])

    ftwhl.ftwhl_dump(pretty_dump, out_filename_phase[1])


if __name__ == "__main__":
    main()
