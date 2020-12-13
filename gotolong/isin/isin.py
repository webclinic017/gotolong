#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import argparse

import gotolong.cutil.cutil

from gotolong.database.database import *


class Isin(Database):
    def __init__(self):
        super(Isin, self).__init__()
        self.isin_table_truncate = False
        self.isin_table_name = "global_isin"
        self.isin_table_dict = {
            "comp_name": "text",
            "comp_industry": "text",
            "comp_ticker": "text",
            "series": "text",
            "comp_isin": "text"
        }
        self.isin_code_both = []
        self.isin_symbol = {}
        self.isin_name_bse = {}
        self.isin_name_nse = {}
        self.isin_industry_dict = {}
        self.isin_industry_list = []
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def isin_table_reload(self, truncate=False):
        self.isin_table_truncate = truncate

    def isin_load_row(self, row, bse_nse):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            if bse_nse == "bse":
                comp_name = row_list[1]
                isin_code = row_list[2]
            else:
                comp_name = row_list[0]
                isin_industry = row_list[1]
                isin_symbol = row_list[2]
                isin_code = row_list[4]

            if isin_code == 'ISIN Code' or isin_code == 'ISIN No.':
                print('skipped header line', row_list)
                return

            comp_name = gotolong.cutil.cutil.normalize_comp_name(comp_name)

            if bse_nse == "nse":
                self.isin_symbol[isin_code] = isin_symbol.upper().strip()
                self.isin_name_nse[isin_code] = comp_name
                self.isin_industry_dict[isin_code] = isin_industry
                # add to industry_list
                if isin_industry not in self.isin_industry_list:
                    self.isin_industry_list.append(isin_industry)
            else:
                self.isin_name_bse[isin_code] = comp_name
            self.isin_code_both.append(isin_code)

            if self.debug_level > 1:
                print('comp_name : ', comp_name, '\n')
                print('isin_code : ', isin_code, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def isin_load_data(self, in_filename, bse_nse):
        table = self.isin_table_name

        if self.isin_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.isin_insert_data(in_filename)
        else:
            print('isin data already loaded in db', row_count)
        print('display db data')
        self.isin_load_db()

    def isin_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        if self.debug_level > 1:
            print('row_list', row_list)
            print('len row_list', len(row_list))

        (comp_name, comp_industry, comp_ticker, series, comp_isin) = row_list

        if comp_ticker == 'Symbol' or comp_industry == "Industry":
            if self.debug_level > 0:
                print('skipped header line', row_list)
            return

        # remove any un-required stuff
        new_row = (comp_name, comp_industry, comp_ticker, series, comp_isin)
        row_bank.append(new_row)

    def isin_insert_data(self, in_filename):
        create_sql = gotolong.cutil.cutil.get_create_sql(self.isin_table_name, self.isin_table_dict)
        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.isin_table_name, self.isin_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # insert row
            row_bank = []
            for line in csvfile:
                self.isin_get_insert_row(line, row_bank)
            print('loaded isin : ', len(row_bank))
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def isin_load_db(self):
        table_name = self.isin_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.isin_load_row(row, "nse")

        # dump industry data
        print('List of high level industries: ')
        for industry_name in sorted(self.isin_industry_list):
            print(industry_name, end=', ')
        print('Industries =', len(self.isin_industry_list))

    def isin_dump_report_full(self, out_filename):
        if self.debug_level > 1:
            print(self.isin_name_bse)
            print(self.isin_name_nse)

        fh = open(out_filename, "w")
        fh.write('isin_code, isin_industry, isin_name_nse, isin_symbol\n')
        for isin_code in sorted(set(self.isin_code_both)):
            p_str = str(isin_code)
            p_str += ', '
            if isin_code in self.isin_industry_dict:
                p_str += self.isin_industry_dict[isin_code]
            else:
                p_str += '-'
            p_str += ', '
            if isin_code in self.isin_name_nse:
                p_str += self.isin_name_nse[isin_code]
                p_str += ', '
                p_str += self.isin_symbol[isin_code]
            else:
                p_str += '-'
                p_str += ', '
                p_str += '-'
            p_str += '\n'
            fh.write(p_str);
        fh.close()

    def isin_dump_report_industry_only(self, out_filename):

        fh = open(out_filename, "w")
        fh.write('isin_industry\n')
        for industry_name in sorted(set(self.isin_industry_list)):
            p_str = str(industry_name)
            p_str += '\n'
            fh.write(p_str)
        fh.close()

    def isin_get_code_by_name(self, req_name):
        req_name = re.sub('\s+', ' ', req_name).strip()
        for isin_code in sorted(self.isin_name_nse):
            # try to find a matching company
            comp_name = self.isin_name_nse[isin_code]
            comp_name = comp_name.strip()
            if re.match(req_name, comp_name):
                if self.debug_level > 1:
                    print('found match : name : ', req_name)
                return isin_code
            if isin_code in self.isin_symbol:
                ticker_symbol = self.isin_symbol[isin_code]
                if req_name.upper() == ticker_symbol:
                    if self.debug_level > 1:
                        print('found ticker : ', req_name)
                    return isin_code
        for isin_code in sorted(self.isin_name_bse):
            # try to find a matching company
            comp_name = self.isin_name_bse[isin_code]
            comp_name = comp_name.strip()
            if re.match(req_name, comp_name):
                if self.debug_level > 1:
                    print('found match : name : ', req_name)
                return isin_code
            if isin_code in self.isin_symbol:
                ticker_symbol = self.isin_symbol[isin_code]
                if req_name.upper() == ticker_symbol:
                    if self.debug_level > 1:
                        print('found ticker : ', req_name)
                    return isin_code
        if self.debug_level > 1:
            print('demat not found : req_name :', req_name, ':')
        return ''

    def isin_get_value_by_code(self, isin_code, value_name):
        if value_name == "name":
            if isin_code in self.isin_name_nse:
                return self.isin_name_nse[isin_code]
            if isin_code in self.isin_name_bse:
                return self.isin_name_bse[isin_code]
            return '-'
        elif value_name == "industry":
            if isin_code in self.isin_name_nse:
                return self.isin_industry_dict[isin_code]
            else:
                return '-'
        else:
            print("isin_get_value_by_code: bad value", value_name)


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
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

    isin = Isin()

    isin.set_debug_level(debug_level)

    if truncate_table:
        isin.isin_table_reload(truncate_table)

    # isin.load_isin_data(bse_filename, 'bse')
    isin.isin_load_data(in_filename_phase[0], 'nse')

    isin.isin_dump_report_full(out_filename_phase[0])
    isin.isin_dump_report_industry_only(out_filename_phase[1])


if __name__ == "__main__":
    main()
