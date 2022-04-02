#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import argparse

import gotolong.cutil.cutil

from gotolong.database.database import *


class Fratio(Database):
    def __init__(self):
        super(Fratio, self).__init__()
        self.fratio_buy = {}
        self.fratio_hold = {}
        self.fratio_enabled = {}
        self.fratio_list = []
        self.fratio_table_truncate = False
        self.fratio_table_name = "global_fratio"
        self.fratio_table_dict = {
            "fratio_name": "text",
            "fratio_buy": "float",
            "fratio_hold": "float",
            "fratio_enabled": "int"
        }
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def fratio_table_reload(self, truncate=False):
        self.fratio_table_truncate = truncate

    def fratio_table_create(self):
        # dump the sql for creation of table
        create_sql = gotolong.cutil.cutil.get_create_sql(self.fratio_table_name, self.fratio_table_dict)
        if self.debug_level > 0:
            print(create_sql)

    def fratio_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            (fratio_name, fratio_buy, fratio_hold, fratio_enabled) = row_list

            self.fratio_list.append(fratio_name)

            self.fratio_buy[fratio_name] = fratio_buy
            self.fratio_hold[fratio_name] = fratio_hold
            self.fratio_enabled[fratio_name] = fratio_enabled

            if self.debug_level > 1:
                print('fratio_name : ', fratio_name, '\n')
                print('fratio_buy : ', fratio_buy, '\n')
                print('fratio_hold : ', fratio_hold, '\n')
                print('fratio_enabled : ', fratio_enabled, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def fratio_load_data(self, in_filename):
        table = self.fratio_table_name

        if self.fratio_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.fratio_insert_data(in_filename)
        else:
            print('fratio data already loaded in db', row_count)
        print('display db data')
        self.fratio_load_data_from_db()

    def fratio_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        if self.debug_level > 1:
            print('row_list', row_list)
            print('len row_list', len(row_list))

        (fratio_name, fratio_buy, fratio_hold, fratio_enabled) = row_list

        if fratio_name == 'fratio_name':
            if self.debug_level > 0:
                print('skipped header line', row_list)
            return

        # remove any un-required stuff
        new_row = (fratio_name, fratio_buy, fratio_hold, fratio_enabled)
        row_bank.append(new_row)

    def fratio_insert_data(self, in_filename):
        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.fratio_table_name, self.fratio_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # insert row
            row_bank = []
            for line in csvfile:
                self.fratio_get_insert_row(line, row_bank)
            print('loaded fratio : ', len(row_bank))
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def fratio_load_data_from_db(self):
        table_name = self.fratio_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.fratio_load_row(row)

    def fratio_dump_report_full(self, out_filename):

        fh = open(out_filename, "w")
        fh.write('fratio_name, fratio_buy, fratio_hold, fratio_enabled\n')
        for fratio_name in self.fratio_list:
            p_str = fratio_name
            p_str += ', '
            p_str += str(self.fratio_buy[fratio_name])
            p_str += ', '
            p_str += str(self.fratio_hold[fratio_name])
            p_str += ', '
            p_str += str(self.fratio_enabled[fratio_name])
            p_str += '\n'
            fh.write(p_str);
        fh.close()


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int,
                        choices=[0, 1, 2, 3])
    parser.add_argument('-t', '--truncate_table', default='False', help='specify to truncate', action='store_true')
    parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
    parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

    args = parser.parse_args()

    debug_level = args.debug_level
    truncate_table = args.truncate_table

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

    if debug_level > 1:
        print('args :', len(sys.argv))

    fratio = Fratio()

    fratio.set_debug_level(debug_level)

    if truncate_table:
        fratio.fratio_table_reload(truncate_table)

    fratio.fratio_load_data(in_filename_phase[0])

    fratio.fratio_dump_report_full(out_filename_phase[0])


if __name__ == "__main__":
    main()
