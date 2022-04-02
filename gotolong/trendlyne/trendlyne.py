#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import gotolong.cutil.cutil
import gotolong.finratio.comp_perf
import gotolong.finratio.comp_price

from gotolong.isin.isin import *
from gotolong.amfi.amfi import *


class Trendlyne(Amfi, Isin):
    def __init__(self):
        super(Trendlyne, self).__init__()
        self.tl_ratio_values = {}
        self.tl_nsecode_list = []
        self.tl_nsecode_industry = {}
        # margin of safety
        self.tl_table_truncate = False
        self.tl_table_name = "global_trendlyne"
        self.debug_level = 0
        self.tl_ratio_name = {
            "Stock": "comp_name",
            "ISIN": "isin",
            "Broker Average Target Rs": "bat",
            "Total Debt to Total Equity Annual": "der",
            "ROCE Annual 3Yr Avg %": "roce3",
            "ROE Annual 3Yr Avg %": "roe3",
            "Dividend payout ratio 2Yr %": "dpr2",
            "Revenue Annual 2Yr Growth %": "sales2",
            "Net Profit 5Yr Growth %": "profit5",
            "Interest Coverage Ratio Annual": "icr",
            "Promoter holding pledge percentage % Qtr": "pledge",
            "3Yr Low Rs": "low_3y",
            "5Yr Low Rs": "low_5y",
            "My Notes": "notes"
        }
        self.tl_ratio_loc = {
            'tl_stock_name': -1,
            'tl_isin': -1,
            'tl_bat': -1,
            'tl_der': -1,
            'tl_roce3': -1,
            'tl_roe3': -1,
            'tl_dpr2': -1,
            'tl_sales2': -1,
            'tl_profit5': -1,
            'tl_icr': -1,
            'tl_pledge': -1,
            'tl_low_3y': -1,
            'tl_low_5y': -1
        }
        self.tl_table_dict = {
            "tl_stock_name": "text",
            "tl_isin": "text",
            "tl_bat": "float",
            "tl_der": "float",
            "tl_roce3": "float",
            "tl_roe3": "float",
            "tl_dpr2": "float",
            "tl_sales2": "float",
            "tl_profit5": "float",
            "tl_icr": "float",
            "tl_pledge": "float",
            "tl_low_3y": "float",
            "tl_low_5y": "float"
        }

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def trendlyne_table_reload(self, truncate_table):
        self.tl_table_truncate = truncate_table

    def trendlyne_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                if self.debug_level > 1:
                    print('ignored empty row', row_list)
                return

            (stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y) = row_list

            if True:
                tl_isin = isin
                tl_nsecode = self.amfi_get_value_by_isin(tl_isin, "ticker")
                self.tl_nsecode_list.append(tl_nsecode)

                for ratio in self.tl_table_dict:
                    if ratio == 'tl_stock_name':
                        self.tl_ratio_values[tl_nsecode, ratio] = stock_name
                    if ratio == 'tl_isin':
                        self.tl_ratio_values[tl_nsecode, ratio] = isin
                    if ratio == 'tl_bat':
                        self.tl_ratio_values[tl_nsecode, ratio] = bat
                    if ratio == 'tl_der':
                        self.tl_ratio_values[tl_nsecode, ratio] = der
                    if ratio == 'tl_roce3':
                        self.tl_ratio_values[tl_nsecode, ratio] = roce3
                    if ratio == 'tl_roe3':
                        self.tl_ratio_values[tl_nsecode, ratio] = roe3
                    if ratio == 'tl_dpr2':
                        self.tl_ratio_values[tl_nsecode, ratio] = dpr2
                    if ratio == 'tl_sales2':
                        self.tl_ratio_values[tl_nsecode, ratio] = sales2
                    if ratio == 'tl_profit5':
                        self.tl_ratio_values[tl_nsecode, ratio] = profit5
                    if ratio == 'tl_icr':
                        self.tl_ratio_values[tl_nsecode, ratio] = icr
                    if ratio == 'tl_pledge':
                        self.tl_ratio_values[tl_nsecode, ratio] = pledge
                    if ratio == 'tl_low_3y':
                        self.tl_ratio_values[tl_nsecode, ratio] = low_3y
                    if ratio == 'tl_low_5y':
                        self.tl_ratio_values[tl_nsecode, ratio] = low_5y
                    if self.debug_level > 1:
                        print('ticker: ', tl_nsecode, 'ratio: ', ratio, 'value: ',
                              self.tl_ratio_values[tl_nsecode, ratio])
        except IndexError:
            print('except ', row)
            traceback.print_exc()
        except KeyError:
            print('except ', row)
            traceback.print_exc()
        except:
            print('except ', row)
            traceback.print_exc()

    def trendlyne_load_data(self, in_filename):
        table = self.tl_table_name

        create_sql = gotolong.cutil.cutil.get_create_sql(self.tl_table_name, self.tl_table_dict)
        if self.debug_level > 0:
            print(create_sql)

        if self.tl_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.trendlyne_insert_data(in_filename)
        else:
            print('trendlyne data already loaded in db', row_count)
        print('display db data')
        self.trendlyne_load_data_from_db()


    def trendlyne_get_insert_row(self, line, row_bank):

        try:

            # remove , comma in double-quoted numbers
            if False:
                new_line = re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', line)
                if line != new_line:
                    if self.debug_level > 1:
                        print('old', line)
                        print('new - without comma', new_line)
                    line = new_line
            # split on comma
            # row_list = line.split(',')

            row_list = line

            # replace ',' with nothing
            for index in range(len(row_list)):
                row_list[index] = row_list[index].replace(',', '')
                # fix for numbers
                if row_list[index] == '-':
                    row_list[index] = 0

            (stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y,
             notes) = row_list

            # double quoted "Stock"
            if stock_name == 'Stock' or stock_name == '"Stock"':
                if self.debug_level > 0:
                    print('skipped header line', row_list)
                    print('len row_list', len(row_list))
                return

            bat = float(bat)
            der = float(der)
            roce3 = float(roce3)
            roe3 = float(roe3)
            dpr2 = float(dpr2)
            sales2 = float(sales2)
            profit5 = float(profit5)
            icr = float(icr)
            pledge = float(pledge)
            low_3y = float(low_3y)
            low_5y = float(low_5y)
            # (funda_reco_type, funda_reco_cause) = self.trendlyne_get_reco(stock_name, isin, bat, der, roce3, roe3, dpr2, sales2,
            #                                                  profit5, icr, pledge, low_3y, low_5y, notes)

            # remove any un-required stuff
            new_row = (
                stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y)
            row_bank.append(new_row)

        except:
            print('except ', line)
            print('len row_list', len(row_list))
            traceback.print_exc()

    def trendlyne_insert_data(self, in_filename):

        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.tl_table_name, self.tl_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            row_bank = []
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                self.trendlyne_get_insert_row(line, row_bank)
            print('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def trendlyne_load_data_from_db(self):
        table = self.tl_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.trendlyne_load_row(row)

    def trendlyne_dump(self, out_filename):

        fh = open(out_filename, "w")

        for ratio in self.tl_ratio_loc:
            fh.write(ratio)
            fh.write(', ')
        fh.write('\n')

        sorted_input = sorted(self.tl_nsecode_list)

        for tl_nsecode in sorted_input:
            p_str = ''
            for ratio in self.tl_ratio_loc:
                p_str += str(self.tl_ratio_values[tl_nsecode, ratio])
                p_str += ', '

            fh.write(p_str)
            fh.write('\n')

        fh.close()


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
    parser.add_argument('-t', '--truncate_table', default='False', help='truncate table', action='store_true')
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

    if debug_level > 1:
        print('args :', len(sys.argv))

    trendlyne = Trendlyne()

    trendlyne.set_debug_level(debug_level)

    if truncate_table:
        trendlyne.trendlyne_table_reload(truncate_table)

    trendlyne.amfi_load_data_from_db()

    trendlyne.trendlyne_load_data(in_filename_phase[0])
    trendlyne.trendlyne_dump(out_filename_phase[0])


if __name__ == "__main__":
    main()
