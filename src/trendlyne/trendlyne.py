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


class Trendlyne(Isin, Amfi):
    def __init__(self):
        super(Trendlyne, self).__init__()
        self.tl_ratio_values = {}
        self.tl_nsecode_list = []
        self.tl_nsecode_industry = {}
        # margin of safety
        self.tl_table_truncate = False
        self.debug_level = 0
        self.tl_ratio_name = {
            "Stock": "name",
            "ISIN": "isin",
            "Broker Average Target Rs": "bat",
            "Broker Average Rating": "bar",
            "Total Debt to Total Equity Annual": "der",
            "ROCE Annual 3Yr Avg %": "roce3",
            "Dividend payout ratio 2Yr %": "dpr2",
            "Promoter holding pledge percentage % Qtr": "pledge"
        }

        self.tl_ratio_loc = {'ticker': -1, 'name': -1, 'isin': -1, 'bat': -1, 'bar': -1}

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
        table = "trendlyne"
        if self.tl_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.trendlyne_insert_data(in_filename)
        else:
            print('trendlyne data already loaded in db', row_count)
        print('display db data')
        self.trendlyne_load_db()

    def trendlyne_insert_data(self, in_filename):
        SQL = """insert into trendlyne(comp_name, comp_isin, comp_bat, comp_bar, comp_der, comp_roce3, comp_dpr2, comp_pledge) values (:comp_name, :comp_isin, :comp_bat, :comp_bar, :comp_der, :comp_roce3, :comp_dpr2, :comp_pledge) """
        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(SQL, csv_reader)
            # commit db changes
            self.db_conn.commit()

    def trendlyne_load_db(self):
        table = "trendlyne"
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
                p_str += self.tl_ratio_values[tl_nsecode, ratio]
                p_str += ', '

            fh.write(p_str)
            fh.write('\n')

        fh.close()
