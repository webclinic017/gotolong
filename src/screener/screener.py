#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import cutil.cutil
import finratio.comp_perf
import finratio.comp_price

from amfi.amfi import *


# class Screener(Isin):
class Screener(Amfi):
    def __init__(self):
        super(Screener, self).__init__()
        self.sc_ratio_values = {}
        self.sc_nsecode = []
        self.sc_nsecode_industry = {} 
        # margin of safety
        self.debug_level = 0
        self.sc_table_truncate = False
        self.sc_table_name = "screener"
        self.sc_ratio_name = {'Name': 'name',
                              'BSE Code': 'bse_code',
                              'NSE Code': 'nse_code',
                              'Industry': 'industry',
                              'Current Price': 'cmp',
                              'Filter': 'filter',
                              'Filter 52 w low': 'filter_52w_low',
                              'up from 52w low': 'up_52w_low',
                              'low price': 'low_52w',
                              'high price': 'high_52w',
                              'Sales': 'sales',
                              'Net profit': 'np',
                              'Market Capitalization': 'mcap',
                              'Debt to equity': 'd2e',
                              'Average return on equity 3Years': 'roe3',
                              'ROCE3yr avg': 'roce3',
                              'Average dividend payout 3years': 'dp3',
                              'Price to Earning': 'pe',
                              'Historical PE 5Years': 'pe5',
                              'PEG Ratio': 'peg',
                              'OPM': 'opm',
                              'Int Coverage': 'ic',
                              'Enterprise Value': 'ev',
                              'Net worth': 'nw',
                              'Reserves': 'reserves',
                              'Return on assets 3years': 'roa3',
                              'Price to book value': 'p2bv',
                              'CMP / OCF': 'p2ocf',
                              'Price to Sales': 'p2sales',
                              'EVEBITDA': 'ev2ebitda',
                              'Dividend Payout Ratio': 'dp',
                              'Dividend yield': 'dy',
                              'Current ratio': 'cr',
                              'Sales growth 5Years': 'sales5',
                              'Profit growth 5Years': 'profit5',
                              'Pledged percentage': 'pledge',
                              'Promoter Holding': 'prom_hold',
                              'Piotroski score': 'piotski'
                              }
        self.sc_ratio_loc = {'rank': -1, 'name': -1, 'bse_code': -1, 'nse_code': -1, 'industry': -1, 'captype': -1,
                             'reco_type': -1, 'reco_cause': -1,
                             'cmp': -1, 'mcap': -1, 'sales': -1, 'np': -1,
                             'd2e': -1, 'roe3': -1, 'roce3': -1, 'dp3': -1, 'dp': -1, 'dy': -1,
                             'pe': -1, 'pe5': -1, 'peg': -1, 'p2bv': -1,
                             'p2sales': -1, 'ev2ebitda': -1, 'ev': -1, 'opm': -1,
                             'cr': -1, 'sales5': -1, 'profit5': -1, 'pledge': -1, 'piotski': -1}
        self.sc_filter_d2e_buy = self.config_der_buy
        self.sc_filter_d2e_hold = self.config_der_hold
        self.sc_filter_dp3_buy = self.config_dpr3_buy
        self.sc_filter_dp3_hold = self.config_dpr3_hold
        self.sc_filter_roce3_buy = self.config_roce3_buy
        self.sc_filter_roce3_hold = self.config_roce3_hold
        self.sc_filter_pledge_buy = self.config_pledge_buy
        self.sc_filter_pledge_hold = self.config_pledge_hold
        self.sc_filter_rank_buy = self.config_rank_buy
        self.sc_filter_rank_hold = self.config_rank_hold

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def screener_table_reload(self, truncate_table):
        self.sc_table_truncate = truncate_table

    def screener_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                if self.debug_level > 1:
                    print('ignored empty row', row_list)
                return

            sc_name = row_list[0].strip()
            if sc_name == 'Name':
                if self.debug_level > 1:
                    print('picked up keys', row_list)
                ratio_name_column_index = 0
                for ratio in row_list:
                    if ratio in self.sc_ratio_name.keys():
                        new_key = self.sc_ratio_name[ratio]
                        if self.debug_level > 0:
                            print('found ratio', ratio, 'mapped to ', new_key)
                        self.sc_ratio_loc[new_key] = ratio_name_column_index
                    else:
                        print('check sc_ratio_name for ', ratio)
                    # increment the ratio name index
                    ratio_name_column_index += 1

                # don't try to delete and iterate original dictionary at the same time. it will become inconsistent.
                loc_dup = dict(self.sc_ratio_loc)
                # delete columns that doesn't have values 
                for ratio in loc_dup:
                    if loc_dup[ratio] == -1:
                        if ratio != 'captype' and ratio != 'rank' and ratio != 'reco_type' and ratio != 'reco_cause':
                            # remove the ratio name from original dictionary
                            self.sc_ratio_loc.pop(ratio)
                            print('removed ratio', ratio)
                    else:
                        if self.debug_level > 0:
                            print('kept ratio', ratio)
                return
            else:
                sc_nsecode = row_list[self.sc_ratio_loc['nse_code']]
                self.sc_nsecode.append(sc_nsecode)

                for ratio in self.sc_ratio_loc:
                    if ratio == 'captype':
                        self.sc_ratio_values[sc_nsecode, ratio] = self.amfi_get_value_by_ticker(sc_nsecode, "captype")
                    elif ratio == 'rank':
                        self.sc_ratio_values[sc_nsecode, ratio] = str(self.amfi_get_value_by_ticker(sc_nsecode, "rank"))
                        if self.debug_level > 1:
                            print('ticker', sc_nsecode, 'rank', self.sc_ratio_values[sc_nsecode, ratio])
                    else:
                        ratio_value = row_list[self.sc_ratio_loc[ratio]]
                        if ratio == 'industry':
                            self.sc_nsecode_industry[sc_nsecode] = ratio_value
                        self.sc_ratio_values[sc_nsecode, ratio] = ratio_value
                    if self.debug_level > 1:
                        print('ticker: ', sc_nsecode, 'ratio: ', ratio, 'value: ',
                              self.sc_ratio_values[sc_nsecode, ratio])
                # figure out reco_type and reco_cause
                reco_type = "BUY"
                reco_cause = "tp, ?"
                ratio = 'd2e'
                value = self.sc_ratio_values[sc_nsecode, ratio]

                # handle missing values
                if value == '':
                    reco_type = "HOLD"
                    reco_cause = ratio + ', ' + 'missing data'
                else:
                    value = float(value)
                    if value > self.sc_filter_d2e_buy:
                        if value > self.sc_filter_d2e_hold:
                            reco_type = "SALE"
                        else:
                            reco_type = "HOLD"
                        reco_cause = ratio + ', ' + str(value)
                        if self.debug_level > 1:
                            print(reco_cause)

                if reco_type != 'Buy':
                    ratio = 'dp3'
                    value = self.sc_ratio_values[sc_nsecode, ratio]
                    if value == '':
                        reco_type = "HOLD"
                        reco_cause = ratio + ', ' + 'missing data'
                    else:
                        value = float(value)
                        if value < self.sc_filter_dp3_buy:
                            if value < self.sc_filter_dp3_hold:
                                reco_type = "SALE"
                            else:
                                reco_type = "HOLD"
                            reco_cause = ratio + ', ' + str(value)
                            if self.debug_level > 1:
                                print(reco_cause)

                if reco_type != 'Buy':
                    ratio = 'roce3'
                    value = self.sc_ratio_values[sc_nsecode, ratio]
                    if value == '':
                        reco_type = "HOLD"
                        reco_cause = ratio + ', ' + 'missing data'
                    else:
                        value = float(value)
                        if value < self.sc_filter_roce3_buy:
                            if value < self.sc_filter_roce3_hold:
                                reco_type = "SALE"
                            else:
                                reco_type = "HOLD"
                            reco_cause = ratio + ', ' + str(value)
                            if self.debug_level > 1:
                                print(reco_cause)

                if reco_type != 'Buy':
                    ratio = 'pledge'
                    value = self.sc_ratio_values[sc_nsecode, ratio]
                    if value == '':
                        reco_type = "HOLD"
                        reco_cause = ratio + ', ' + 'missing data'
                    else:
                        value = float(value)
                        if value > self.sc_filter_pledge_buy:
                            if value > self.sc_filter_pledge_hold:
                                reco_type = "SALE"
                            else:
                                reco_type = "HOLD"
                            reco_cause = ratio + ', ' + str(value)
                            if self.debug_level > 1:
                                print(reco_cause)

                if reco_type != 'Buy':
                    ratio = 'rank'
                    value = self.sc_ratio_values[sc_nsecode, ratio]
                    if value == '':
                        reco_type = "HOLD"
                        reco_cause = ratio + ', ' + 'missing data'
                    else:
                        value = float(value)
                        if value > self.sc_filter_rank_buy:
                            if value > self.sc_filter_rank_hold:
                                reco_type = "SALE"
                            else:
                                reco_type = "HOLD"
                            reco_cause = 'rank, ' + str(value)
                            if self.debug_level > 1:
                                print(reco_cause)

                # store recommendation
                self.sc_ratio_values[sc_nsecode, "reco_type"] = reco_type
                self.sc_ratio_values[sc_nsecode, "reco_cause"] = reco_cause

        except IndexError:
            print('except ', row)
            traceback.print_exc()
        except KeyError:
            print('except ', row)
            traceback.print_exc()
        except ValueError:
            print('except ', row)
            traceback.print_exc()
        except:
            print('except ', row)
            traceback.print_exc()

    def screener_load_data(self, sc_filename):
        with open(sc_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.screener_load_row(row)

    def screener_load_data(self, in_filename):
        table = self.sc_table_name
        if self.sc_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.screener_insert_data(in_filename)
        else:
            print('screener data already loaded in db', row_count)
        print('display db data')
        self.screener_load_db()

    def screener_insert_data(self, in_filename):
        SQL = "insert into "
        SQL += self.sc_table_name
        SQL += "("

        iter = 0
        for ratio in self.sc_ratio_name:
            SQL += self.sc_ratio_name[ratio]
            if iter != len(self.sc_ratio_name) - 1:
                SQL += ","
            iter += 1

        SQL += ") values("

        iter = 0
        for ratio in self.sc_ratio_name:
            SQL += ":"
            SQL += self.sc_ratio_name[ratio]
            if iter != len(self.sc_ratio_name) - 1:
                SQL += ","
            iter += 1
        SQL += ")"

        print(SQL)

        create_sql = "create table if not exists "
        create_sql += self.sc_table_name
        create_sql += "("

        iter = 0
        for ratio in self.sc_ratio_name:
            create_sql += self.sc_ratio_name[ratio]
            if iter != len(self.sc_ratio_name) - 1:
                create_sql += " text,"
            iter += 1
        create_sql += " text)"
        print(create_sql)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(SQL, csv_reader)
            # commit db changes
            self.db_conn.commit()

    def screener_load_db(self):
        table = self.sc_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.screener_load_row(row)

    def screener_dump_phase1(self, out_filename, filter_rows=False, ticker_only=False, hold_filename=False,
                     sale_filename=False, reco_filename=False):

        fh = open(out_filename, "w")

        if hold_filename:
            fh_hold = open(hold_filename, "w")

        if sale_filename:
            fh_sale = open(sale_filename, "w")

        if reco_filename:
            fh_reco = open(reco_filename, "w")

        if not ticker_only:
            for ratio in self.sc_ratio_loc:
                fh.write(ratio)
                fh.write(', ')
            fh.write('\n')

        if filter_rows:
            # sorted_input = sorted(self.sc_nsecode_industry, key=self.sc_nsecode_industry.__getitem__)
            sorted_input = sorted(self.sc_nsecode)
        else:
            sorted_input = sorted(self.sc_nsecode)

        for sc_nsecode in sorted_input:
            p_str = ''
            for ratio in self.sc_ratio_loc:
                p_str += self.sc_ratio_values[sc_nsecode, ratio]
                p_str += ', '

            reco_type = self.sc_ratio_values[sc_nsecode, "reco_type"]
            reco_cause = self.sc_ratio_values[sc_nsecode, "reco_cause"]

            reco_str = sc_nsecode + ',' + reco_type + ',' + reco_cause + '\n'

            if reco_filename:
                fh_reco.write(reco_str)

            if reco_type == "HOLD" or reco_type == "SALE":
                if reco_type == "HOLD" and hold_filename:
                    fh_hold.write(reco_str)
                elif reco_type == "SALE" and sale_filename:
                    fh_sale.write(reco_str)
            else:
                if ticker_only:
                    fh.write(sc_nsecode)
                else:
                    fh.write(p_str)
                fh.write('\n')

        fh.close()

        if hold_filename:
            fh_hold.close()

        if sale_filename:
            fh_sale.close()

        if reco_filename:
            fh_reco.close()

    def screener_dump_phase2(self, out_filename):
        self.screener_dump_phase1(out_filename, True)

    def screener_dump_phase3(self, out_filename, hold_filename, sale_filename, reco_filename):
        self.screener_dump_phase1(out_filename, True, True, hold_filename, sale_filename, reco_filename)
