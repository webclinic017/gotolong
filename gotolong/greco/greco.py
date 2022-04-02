#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import argparse

import gotolong.cutil.cutil

from gotolong.database.database import *
from gotolong.trendlyne.trendlyne import *
from gotolong.fratio.fratio import *
from gotolong.isin.isin import *


class Gfundareco(Fratio, Trendlyne, Isin):
    def __init__(self):
        super(Gfundareco, self).__init__()
        self.gfunda_reco_ticker_list = []
        self.gfunda_reco_isin = {}
        self.gfunda_reco_type = {}
        self.gfunda_reco_cause = {}
        self.gfunda_reco_table_truncate = False
        self.gfunda_reco_table_name = "global_funda_reco"
        self.gfunda_reco_table_dict = {
            "funda_reco_ticker": "text",
            "funda_reco_isin": "text",
            "funda_reco_type": "text",
            "funda_reco_cause": "text"
        }
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def gfunda_reco_table_reload(self, truncate=False):
        self.gfunda_reco_table_truncate = truncate

    def gfunda_reco_table_create(self):
        # dump the sql for creation of table
        create_sql = gotolong.cutil.cutil.get_create_sql(self.gfunda_reco_table_name, self.gfunda_reco_table_dict)
        if self.debug_level > 0:
            print(create_sql)

    def gfunda_reco_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            (funda_reco_ticker, funda_reco_isin, funda_reco_type, funda_reco_cause) = row_list

            self.gfunda_reco_ticker_list.append(funda_reco_ticker)
            self.gfunda_reco_isin[funda_reco_ticker] = funda_reco_isin
            self.gfunda_reco_type[funda_reco_ticker] = funda_reco_type
            self.gfunda_reco_cause[funda_reco_ticker] = funda_reco_cause

            if self.debug_level > 1:
                print('ticker : ', funda_reco_ticker, '\n')
                print('funda_reco_type : ', funda_reco_type, '\n')
                print('funda_reco_cause : ', funda_reco_cause, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def gfunda_reco_load_data(self):
        table = self.gfunda_reco_table_name

        if self.gfunda_reco_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.gfunda_reco_fill_data()
        else:
            print('gfundareco data already loaded in db', row_count)
        print('display db data')
        self.gfunda_reco_load_data_from_db()

    def gfunda_reco_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        if self.debug_level > 1:
            print('row_list', row_list)
            print('len row_list', len(row_list))

        if funda_reco_type == 'Reco Type' or funda_reco_cause == "Reco Cause":
            if self.debug_level > 0:
                print('skipped header line', row_list)
            return

        # remove any un-required stuff
        new_row = (funda_reco_ticker, funda_reco_isin, funda_reco_type, funda_reco_cause)
        row_bank.append(new_row)

    def gfunda_reco_fill_data(self):
        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.gfunda_reco_table_name, self.gfunda_reco_table_dict)

        cursor = self.db_conn.cursor()

        # insert row
        row_bank = []

        # fill data from other table
        sorted_input = sorted(self.tl_nsecode_list)

        # breakpoint()

        for tl_nsecode in sorted_input:
            (funda_reco_type, funda_reco_cause) = self.gfunda_reco_get_reco(
                self.tl_ratio_values[tl_nsecode, 'tl_stock_name'], self.tl_ratio_values[tl_nsecode, 'tl_isin'],
                self.tl_ratio_values[tl_nsecode, 'tl_bat'], self.tl_ratio_values[tl_nsecode, 'tl_der'],
                self.tl_ratio_values[tl_nsecode, 'tl_roce3'], self.tl_ratio_values[tl_nsecode, 'tl_roe3'],
                self.tl_ratio_values[tl_nsecode, 'tl_dpr2'], self.tl_ratio_values[tl_nsecode, 'tl_sales2'],
                self.tl_ratio_values[tl_nsecode, 'tl_profit5'], self.tl_ratio_values[tl_nsecode, 'tl_icr'],
                self.tl_ratio_values[tl_nsecode, 'tl_pledge'], self.tl_ratio_values[tl_nsecode, 'tl_low_3y'],
                self.tl_ratio_values[tl_nsecode, 'tl_low_5y'], 'notes')

            funda_reco_ticker = tl_nsecode
            funda_reco_isin = self.tl_ratio_values[tl_nsecode, 'tl_isin']
            new_row = (funda_reco_ticker, funda_reco_isin, funda_reco_type, funda_reco_cause)
            row_bank.append(new_row)

        print('loaded gfundareco : ', len(row_bank))
        # insert row
        cursor.executemany(insert_sql, row_bank)
        # commit db changes
        self.db_conn.commit()

    def gfunda_reco_load_data_from_db(self):
        table_name = self.gfunda_reco_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.gfunda_reco_load_row(row)

    def gfunda_reco_get_reco(self, stock_name, isin, bat, der, roce3,
                             roe3, dpr2, sales2, profit5, icr,
                             pledge, low_3y, low_5y, notes):
        ignore_der = False
        # skip debt for Financial Services like Bank/NBFC.
        if isin in self.isin_industry_dict:
            if self.debug_level > 1:
                print('tl', 'isin', isin, 'industry', self.isin_industry[isin])
            if self.isin_industry_dict[isin] == 'FINANCIAL SERVICES':
                ignore_der = True
        else:
            print(isin, 'not found in isin db')

        funda_reco_type = 'NONE'
        funda_reco_cause = ''

        if ignore_der:
            b_c1 = True
        else:
            b_c1 = der <= self.fratio_buy['der']

        b_c2 = roce3 >= self.fratio_buy['roce3']
        b_c3 = dpr2 >= self.fratio_buy['dpr2']
        b_c4 = sales2 >= self.fratio_buy['sales2']
        b_c5 = profit5 >= self.fratio_buy['profit5']
        b_c6 = pledge <= self.fratio_buy['pledge']

        # if isin == 'INE079A01024':
        #    breakpoint()

        if not b_c1:
            funda_reco_cause += " "
            funda_reco_cause = "-B(der)"
        if not b_c2:
            funda_reco_cause += " "
            funda_reco_cause = "-B(roce3)"
        if not b_c3:
            funda_reco_cause += " "
            funda_reco_cause = "-B(dpr2)"
        if not b_c4:
            funda_reco_cause += " "
            funda_reco_cause = "-B(sales)"
        if not b_c5:
            funda_reco_cause += " "
            funda_reco_cause = "-B(profit5)"
        if not b_c6:
            funda_reco_cause += " "
            funda_reco_cause = "-B(pledge)"

        if (b_c1 and b_c2 and b_c3 and b_c4 and b_c5 and b_c6):
            funda_reco_type = "BUY"
            funda_reco_cause = "ALL"
            return (funda_reco_type, funda_reco_cause)
        else:
            s_c1 = der > self.fratio_hold['der']
            s_c2 = roce3 < self.fratio_hold['roce3']
            s_c3 = dpr2 < self.fratio_hold['dpr2']
            s_c4 = sales2 < self.fratio_hold['sales2']
            s_c5 = profit5 < self.fratio_hold['profit5']
            s_c6 = pledge > self.fratio_hold['pledge']
            # avoid NONE
            funda_reco_cause_buy = funda_reco_cause
            funda_reco_cause = ''

            if s_c1:
                if not ignore_der:
                    funda_reco_cause += " "
                    funda_reco_cause += "S(der)"
            if s_c2:
                funda_reco_cause += " "
                funda_reco_cause += "S(roce3)"
            if s_c3:
                funda_reco_cause += " "
                funda_reco_cause += "S(dpr2)"
            if s_c4:
                funda_reco_cause += " "
                funda_reco_cause += "S(sales2)"
            if s_c5:
                funda_reco_cause += " "
                funda_reco_cause += "S(profit5)"
            if s_c6:
                funda_reco_cause += " "
                funda_reco_cause += "S(pledge)"

            if funda_reco_cause == '':
                funda_reco_type = "HOLD"
            else:
                funda_reco_type = "SALE"

        if funda_reco_type == 'HOLD':
            h_c1 = (der > self.fratio_buy['der'] and der <= self.fratio_hold['der'])
            # fixed the bug here to get the cause for HOLD
            h_c2 = (roce3 < self.fratio_buy['roce3'] and roce3 >= self.fratio_hold['roce3'])
            h_c3 = (dpr2 < self.fratio_buy['dpr2'] and dpr2 >= self.fratio_hold['dpr2'])
            h_c4 = (sales2 < self.fratio_buy['sales2'] and sales2 >= self.fratio_hold['sales2'])
            h_c5 = (profit5 < self.fratio_buy['profit5'] and profit5 >= self.fratio_hold['profit5'])
            h_c6 = (pledge > self.fratio_buy['pledge'] and pledge <= self.fratio_hold['pledge'])

            if h_c1:
                if not ignore_der:
                    funda_reco_cause += " "
                    funda_reco_cause += "H(der)"
            if h_c2:
                funda_reco_cause += " "
                funda_reco_cause += "H(roce3)"
            if h_c3:
                funda_reco_cause += " "
                funda_reco_cause += "H(dpr2)"
            if h_c4:
                funda_reco_cause += " "
                funda_reco_cause += "H(sales2)"
            if h_c5:
                funda_reco_cause += " "
                funda_reco_cause += "H(profit5)"
            if h_c6:
                funda_reco_cause += " "
                funda_reco_cause += "H(pledge)"

            # for debugging
            if funda_reco_cause == '':
                funda_reco_cause = funda_reco_cause_buy

        return (funda_reco_type, funda_reco_cause)

    def gfunda_reco_dump_report_full(self, out_filename):

        fh = open(out_filename, "w")
        fh.write('funda_reco_ticker, funda_reco_isin, funda_reco_type, funda_reco_cause\n')
        for funda_reco_ticker in self.gfunda_reco_ticker_list:
            p_str = funda_reco_ticker
            p_str += ', '
            p_str += self.gfunda_reco_isin[funda_reco_ticker]
            p_str += ', '
            p_str += self.gfunda_reco_type[funda_reco_ticker]
            p_str += ', '
            p_str += self.gfunda_reco_cause[funda_reco_ticker]
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
    parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

    args = parser.parse_args()

    debug_level = args.debug_level
    truncate_table = args.truncate_table

    # dummy assignment
    in_filename_phase = []
    out_filename_phase = []

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

    gfundareco = Gfundareco()

    gfundareco.set_debug_level(debug_level)

    if truncate_table:
        gfundareco.gfunda_reco_table_reload(truncate_table)

    gfundareco.amfi_load_data_from_db()
    gfundareco.isin_load_data_from_db()

    gfundareco.trendlyne_load_data_from_db()

    gfundareco.fratio_load_data_from_db()

    gfundareco.gfunda_reco_load_data()

    gfundareco.gfunda_reco_dump_report_full(out_filename_phase[0])


if __name__ == "__main__":
    main()
