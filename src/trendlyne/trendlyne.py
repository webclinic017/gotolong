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
            'low_5y': -1,
            'reco_type': -1,
            'reco_cause': -1
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
            "low_5y": "float",
            'reco_type': "text",
            'reco_cause': "text"
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

            (stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y, reco_type,
             reco_cause) = row_list

            if True:
                tl_isin = isin
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
                        ratio_value = bat
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

    def trendlyne_get_reco(self, stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge,
                           low_3y, low_5y, notes):

        b_c1 = der <= self.config_der_buy
        b_c2 = roce3 >= self.config_roce3_buy
        b_c3 = dpr2 >= self.config_dpr2_buy
        b_c4 = sales2 >= self.config_sales2_buy
        b_c5 = profit5 >= self.config_profit5_buy
        b_c6 = pledge <= self.config_pledge_buy

        reco_type = 'NONE'
        reco_cause = 'NONE'

        if (b_c1 and b_c2 and b_c3 and b_c4 and b_c5 and b_c6):
            reco_type = "BUY"
            reco_cause = "ALL"
            return (reco_type, reco_cause)
        else:
            s_c1 = der > self.config_der_hold
            s_c2 = roce3 < self.config_roce3_hold
            s_c3 = dpr2 < self.config_dpr2_hold
            s_c4 = sales2 < self.config_sales2_hold
            s_c5 = profit5 < self.config_profit5_hold
            s_c6 = pledge > self.config_pledge_hold
            reco_cause = ''
            if s_c1:
                reco_cause += " "
                reco_cause += "der"
            if s_c2:
                reco_cause += " "
                reco_cause += "roce3"
            if s_c3:
                reco_cause += " "
                reco_cause += "dpr2"
            if s_c4:
                reco_cause += " "
                reco_cause += "sales2"
            if s_c5:
                reco_cause += " "
                reco_cause += "profit5"
            if s_c6:
                reco_cause += " "
                reco_cause += "pledge"

            if reco_cause == '':
                reco_type = "HOLD"
            else:
                reco_type = "SALE"

        if reco_type == 'HOLD':
            h_c1 = (der > self.config_der_buy and der <= self.config_der_hold)
            h_c2 = (roce3 > self.config_roce3_buy and roce3 >= self.config_roce3_hold)
            h_c3 = (dpr2 < self.config_dpr2_buy and dpr2 >= self.config_dpr2_hold)
            h_c4 = (sales2 < self.config_sales2_buy and sales2 >= self.config_sales2_hold)
            h_c5 = (profit5 < self.config_profit5_buy and profit5 >= self.config_profit5_hold)
            h_c6 = (pledge > self.config_pledge_buy and pledge <= self.config_pledge_hold)

            reco_cause = ''
            if h_c1:
                reco_cause += " "
                reco_cause += "der"
            if h_c2:
                reco_cause += " "
                reco_cause += "roce3"
            if h_c3:
                reco_cause += " "
                reco_cause += "dpr2"
            if h_c4:
                reco_cause += " "
                reco_cause += "sales2"
            if h_c5:
                reco_cause += " "
                reco_cause += "profit5"
            if h_c6:
                reco_cause += " "
                reco_cause += "pledge"

        return (reco_type, reco_cause)

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
            (reco_type, reco_cause) = self.trendlyne_get_reco(stock_name, isin, bat, der, roce3, roe3, dpr2, sales2,
                                                              profit5, icr, pledge, low_3y, low_5y, notes)

            # remove any un-required stuff
            new_row = (
                stock_name, isin, bat, der, roce3, roe3, dpr2, sales2, profit5, icr, pledge, low_3y, low_5y, reco_type,
                reco_cause)
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
