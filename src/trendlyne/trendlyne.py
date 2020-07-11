#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import cutil.cutil
import finratio.comp_perf
import finratio.comp_price

from isin.isin import *
from amfi.amfi import *


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
            'stock_name': -1,
            'isin': -1,
            'bat': -1,
            'der': -1,
            'roce3': -1,
            'roe3': -1,
            'dpr2': -1,
            'sales2': -1,
            'profit5': -1,
            'icr': -1,
            'pledge': -1,
            'low_3y': -1,
            'low_5y': -1
        }
        self.tl_table_dict = {
            "stock_name": "text",
            "isin": "text",
            "bat": "float",
            "der": "float",
            "roce3": "float",
            "roe3": "float",
            "dpr2": "float",
            "sales2": "float",
            "profit5": "float",
            "icr": "float",
            "pledge": "float",
            "low_3y": "float",
            "low_5y": "float"
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

            tl_name = row_list[0].strip()
            if tl_name == 'Stock':
                if self.debug_level > 1:
                    print('picked up keys', row_list)
                ratio_name_column_index = 0
                for ratio in row_list:
                    if ratio in self.tl_ratio_name.keys():
                        new_key = self.tl_ratio_name[ratio]
                        if self.debug_level > 0:
                            print('found ratio', ratio, 'mapped to ', new_key)
                        self.tl_ratio_loc[new_key] = ratio_name_column_index
                    else:
                        print('check tl_ratio_name for ', ratio)
                    # increment the ratio name index
                    ratio_name_column_index += 1

                # don't try to delete and iterate original dictionary at the same time. it will become inconsistent.
                loc_dup = dict(self.tl_ratio_loc)
                # delete columns that doesn't have values
                for ratio in loc_dup:
                    if loc_dup[ratio] == -1:
                        if ratio != 'captype' and ratio != "mcrank" and ratio != 'ticker':
                            # remove the ratio name from original dictionary
                            self.tl_ratio_loc.pop(ratio)
                            print('removed ratio', ratio)
                    else:
                        if self.debug_level > 0:
                            print('kept ratio', ratio)
                return
            else:
                tl_isin = row_list[self.tl_ratio_loc['isin']]
                tl_nsecode = self.amfi_get_value_by_isin(tl_isin, "ticker")
                self.tl_nsecode_list.append(tl_nsecode)

                for ratio in self.tl_ratio_loc:
                    if ratio == 'ticker':
                        self.tl_ratio_values[tl_nsecode, ratio] = tl_nsecode
                    elif ratio == 'captype':
                        self.tl_ratio_values[tl_nsecode, ratio] = self.amfi_get_value_by_ticker(tl_nsecode, "captype")
                    elif ratio == 'rank':
                        self.tl_ratio_values[tl_nsecode, ratio] = str(self.amfi_get_value_by_ticker(tl_nsecode, "rank"))
                        if self.debug_level > 0:
                            print('ticker', tl_nsecode, 'rank', self.tl_ratio_values[tl_nsecode, ratio])
                    elif ratio == 'bat':
                        ratio_value = row_list[self.tl_ratio_loc[ratio]]
                        self.tl_ratio_values[tl_nsecode, ratio] = str(cutil.cutil.get_number(ratio_value))
                    else:
                        ratio_value = row_list[self.tl_ratio_loc[ratio]]
                        if ratio == 'industry':
                            self.tl_nsecode_industry[tl_nsecode] = ratio_value
                        self.tl_ratio_values[tl_nsecode, ratio] = ratio_value
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

        create_sql = cutil.cutil.get_create_sql(self.tl_table_name, self.tl_table_dict)
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
        self.trendlyne_load_db()

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

            # remove any un-required stuff
            new_row = (
            stock_name, isin, float(bat), der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y)
            row_bank.append(new_row)

        except:
            print('except ', line)
            print('len row_list', len(row_list))
            traceback.print_exc()

    def trendlyne_insert_data(self, in_filename):

        insert_sql = cutil.cutil.get_insert_sql(self.tl_table_name, self.tl_table_dict)

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

    def trendlyne_load_db(self):
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
