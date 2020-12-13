#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3

import logging

import traceback

import argparse

import gotolong.cutil.cutil

from prettytable import PrettyTable

from gotolong.database.database import *


class Corpact(Database):
    def __init__(self):
        super(Corpact, self).__init__()
        # isin number
        self.corpact_ticker_list = []
        self.corpact_total = {}
        self.corpact_bonus = {}
        self.corpact_buyback = {}
        self.corpact_dividend = {}
        self.debug_level = 0
        self.corpact_table_truncate = False
        self.corpact_table_name = "global_corpact"
        self.corpact_table_dict = {
            "security_name": "text",
            "total_score": "int",
            "bonus_score": "int",
            "buyback_score": "int",
            "dividend_score": "int"
        }

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def corpact_table_reload(self, truncate=False):
        self.corpact_table_truncate = truncate

    def corpact_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                logging.info('ignored empty row %s', row_list)
                return

            security_name = row_list[0].strip()

            if security_name == 'security_name':
                logging.info('skipped header line %s', row_list)
                return

            total_score = row_list[1]
            bonus_score = row_list[2]
            buyback_score = row_list[3]
            dividend_score = row_list[4]

            logging.debug('security_name : %s total_score: %s bonus_score : %s buyback_score : %s dividend_score : %s',
                          security_name, total_score, bonus_score, buyback_score, dividend_score)

            nse_ticker = security_name

            self.corpact_total[nse_ticker] = total_score
            self.corpact_bonus[nse_ticker] = bonus_score
            self.corpact_buyback[nse_ticker] = buyback_score
            self.corpact_dividend[nse_ticker] = dividend_score
            self.corpact_ticker_list.append(nse_ticker)

        except IndexError:
            logging.error('except %s', row)
        except:
            logging.error('except %s', row)
            traceback.print_exc()

    def corpact_store_data_to_db(self, in_filename):
        table = self.corpact_table_name

        if self.corpact_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_amfi_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.corpact_insert_data(in_filename)
        else:
            logging.info('corpact data already loaded in db %d', row_count)

    def corpact_get_insert_row(self, line, row_bank):

        # split on comma
        line = re.sub(',",', ',', line)
        line = re.sub('"', '', line)
        row_list = line.split(',')

        logging.debug('row_list %s', row_list)
        logging.debug('len row_list %d', len(row_list))

        (security_name, total_score, bonus_score, buyback_score, dividend_score) = row_list

        # remove new line character from end
        dividend_score = dividend_score.strip('\n')

        if security_name == 'security_name':
            logging.info('skipped header line %s', row_list)
            logging.info('len row_list %d', len(row_list))
            return

        # remove any un-required stuff
        new_row = (security_name, total_score, bonus_score, buyback_score, dividend_score)
        row_bank.append(new_row)

    def corpact_insert_data(self, in_filename):

        create_sql = gotolong.cutil.cutil.get_create_sql(self.corpact_table_name, self.corpact_table_dict)
        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.corpact_table_name, self.corpact_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            # insert row
            row_bank = []
            for line in csvfile:
                self.corpact_get_insert_row(line, row_bank)
            logging.info('loaded entries %s', len(row_bank))
            logging.info('from %s', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def corpact_load_data_from_db(self):
        table = self.corpact_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug('%s', row)
            self.corpact_load_row(row)

    def corpact_dump(self, pretty_dump, out_filename):

        logging.info('output filename %s', out_filename)

        pt = PrettyTable()
        pt.field_names = ["security_name", "corpact_score", "bonus_score", "buyback_score", "dividend_score"]

        fh = open(out_filename, "w")

        dump_first_rec = True
        for ticker in sorted(self.corpact_total, key=self.corpact_total.__getitem__, reverse=True):
            if dump_first_rec:
                dump_first_rec = False
                logging.debug('ticker  %s', ticker)

            row_list = [ticker]
            row_list.append(str(self.corpact_total[ticker]))
            row_list.append(str(self.corpact_bonus[ticker]))
            row_list.append(str(self.corpact_buyback[ticker]))
            row_list.append(str(self.corpact_dividend[ticker]))

            pt.add_row(row_list)

        if pretty_dump:
            fh.write(str(pt))
            fh.close()

    def corpact_export(self, export_to_file, out_filename):

        logging.info('output filename %s', out_filename)

        field_names = ["security_name", "total_score", "bonus_score", "buyback_score", "dividend_score"]

        if export_to_file:
            fh = open(out_filename, "w")
            p_hdr = ','.join(field_names)
            p_hdr += '\n'
            fh.write(p_hdr)

        dump_first_rec = True
        for ticker in sorted(self.corpact_total, key=self.corpact_total.__getitem__, reverse=True):
            if dump_first_rec:
                logging.debug('ticker  %s', ticker)
                dump_first_rec = False

            row_list = [ticker]
            row_list.append(str(self.corpact_total[ticker]))
            row_list.append(str(self.corpact_bonus[ticker]))
            row_list.append(str(self.corpact_buyback[ticker]))
            row_list.append(str(self.corpact_dividend[ticker]))

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
            print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> ... ")
            sys.exit(1)

        print('args :', len(sys.argv))

        corpact = Corpact()

        corpact.set_log_level(log_level)

        if truncate_table:
            corpact.corpact_table_reload(truncate_table)

        if save_to_db:
            corpact.corpact_store_data_to_db(in_filename_phase[0])

        corpact.corpact_load_data_from_db()

        corpact.corpact_export(export_to_file, out_filename_phase[0])

        corpact.corpact_dump(pretty_dump, out_filename_phase[1])

        print('end of main')


if __name__ == "__main__":
    main()
