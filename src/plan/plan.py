# !/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from amfi.amfi import *

class Plan(Amfi):

    def __init__(self):
        super(Plan, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.plan_multiply = 1 
        self.plan_comp_units = {}
        self.plan_indu_units = {}
        self.debug_level = 0
        self.db_table_reload = False
        self.last_row = ""
        self.plan_captype_comp_count_dict = {}
        print('init : Plan')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def set_table_reload(self, truncate=False):
        self.db_table_reload = truncate 

    def load_plan_row(self, row):
        try:
            row_list = row

            if row_list[0].strip() == 'comp_industry':
                return
            if row_list[0].strip() == 'AaStatistics':
                return
            comp_industry = row_list[0]
            comp_name = row_list[1]
            ticker = row_list[2]
            comp_selected = cutil.cutil.get_number(row_list[3])
            comp_desc = row_list[4]
            if comp_industry in self.plan_indu_units.keys():
                self.plan_indu_units[comp_industry] = self.plan_indu_units[comp_industry] + comp_selected
            else:
                self.plan_indu_units[comp_industry] = comp_selected
            if self.debug_level > 0:
                print('industry ', comp_industry)
                print('company name', comp_name)
                print('company selected', comp_selected)
                print('company desc', comp_desc)
            # use ticker as an input
            # isin = self.amfi_get_isin_by_name(comp_ticker)
            if self.debug_level > 0:
                print(ticker, comp_name)

            captype = self.amfi_get_value_by_ticker(ticker, "captype")
            if self.debug_level > 0:
                print(ticker, captype)

            if comp_selected >= 0:
                self.plan_comp_units[ticker] = comp_selected
                self.plan_comp_units[ticker] = self.plan_comp_units[ticker] * self.plan_multiply
            else:
                self.plan_comp_units[ticker] = 0

            if captype in self.plan_captype_comp_count_dict:
                self.plan_captype_comp_count_dict[captype] += 1
            else:
                self.plan_captype_comp_count_dict[captype] = 1
            return
        except TypeError:
            print('except : TypeError : ', row, "\n")
            traceback.print_exc()
        except ValueError:
            print('except : ValueError :', row, "\n")
            traceback.print_exc()
        except IndexError:
            print('except : IndexError : ', row, "\n")
            traceback.print_exc()

    def load_plan_data(self, in_filename):
        table = "plan"
        if self.db_table_reload:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.insert_plan_data(in_filename)
        else:
            print('plan data already loaded in db', row_count)
        print('display db data')
        self.load_plan_db()

    def insert_plan_data(self, in_filename):
        SQL = """insert into plan(comp_industry, comp_name, comp_ticker, comp_selected, comp_desc) values (:comp_industry, :comp_name, :comp_ticker, :comp_selected, :comp_desc) """
        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(SQL, csv_reader)
            # commit db changes
            self.db_conn.commit()

    def load_plan_db(self):
        table = "plan"
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1 :
                print(row)
            self.load_plan_row(row)

    def plan_dump_ticker(self, out_filename):
        lines = []
        fh = open(out_filename, "w")
        sorted_items = sorted(self.plan_comp_units, key=self.plan_comp_units.__getitem__, reverse=True)

        for ticker in sorted_items:
            try:
                if int(self.plan_comp_units[ticker]) > 0:
                    p_str = ticker 
                    p_str += '\n'
                    lines.append(p_str)
            except ValueError:
                print('except : ValueError :', comp_name)
        lines.sort()
        fh.writelines(lines)
        return

    def plan_dump_generic(self, out_filename, sort_type_rank = None, plus_holdings = None, zero_holdings = None):
        total_units = 0
        cap_units = {}
        fh = open(out_filename, "w")
        fh.write('comp_name, ticker, isin, plan_units_1k, rank, captype, mcap\n')
        if sort_type_rank:
            sorted_items = sorted(self.amfi_rank, key=self.amfi_rank.__getitem__)
            if self.debug_level > 2:
                print(sorted_items)
        else:
            sorted_items = sorted(self.plan_comp_units, key=self.plan_comp_units.__getitem__, reverse=True)

        for ticker in sorted_items:
            try:
                # isin = self.amfi_get_isin_by_name(comp_name)
                comp_name = self.amfi_get_value_by_ticker(ticker, "cname")
                if self.debug_level >= 2:
                    print(comp_name)
                if ticker in self.plan_comp_units:
                    units_1k = int(self.plan_comp_units[ticker])
                else:
                    units_1k = 0
                if self.debug_level >= 2:
                    print(units_1k)
                mcap = self.amfi_get_value_by_ticker(ticker, "mcap")
                captype = self.amfi_get_value_by_ticker(ticker, "captype")
                if self.debug_level > 0:
                    print(ticker, captype)
                rank = self.amfi_get_value_by_ticker(ticker, "rank")
            except ValueError:
                print('except : ValueError :', comp_name)

            if plus_holdings:
                if units_1k <= 0 :
                    continue

            if zero_holdings :
                if units_1k > 0 :
                    continue

            if sort_type_rank:
                if int(rank) > 500 and units_1k <= 0:
                    continue

            p_str = comp_name
            p_str += ', '
            p_str += ticker
            p_str += ', '
            isin = self.amfi_get_value_by_ticker(ticker, "isin")
            p_str += isin 
            p_str += ', '
            if ticker in self.plan_comp_units:
                p_str += str(self.plan_comp_units[ticker])
            else:
                p_str += '0'
            p_str += ', '
            p_str += str(rank)
            p_str += ', '
            p_str += captype
            p_str += ', '
            p_str += str(mcap)
            p_str += '\n'
            fh.write(p_str)

        # Current portfolio distribution

        # captype comp count
        ccc_dict = self.plan_captype_comp_count_dict
        if self.debug_level > 0:
            print(ccc_dict)

        total_units = 0
        # calculate total_units
        # fix missing values
        for captype in self.amfi_captype_list:
            if captype not in ccc_dict:
                ccc_dict[captype] = 0
            else:
                total_units += int(ccc_dict[captype])

        p_str = 'Summary'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += str(total_units)
        p_str += ', '
        try:
            p_str += 'large ' + str(int(round(float((ccc_dict['Large Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'mid ' + str(int(round(float((ccc_dict['Mid Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'small ' + str(int(round(float(((ccc_dict['Small Cap'] + ccc_dict['Micro Cap'] + ccc_dict[
                'Nano Cap'] + ccc_dict['Unknown Cap']) * 100.0) / total_units)))) + ' %'
            p_str += '\n'
        except KeyError:
            print('except KeyError')
            traceback.print_exc()
        except TypeError:
            print('except TypeError', ticker)
            traceback.print_exc()

        fh.write(p_str)

        # Ideal portfolio distribution
        p_str = 'Ideal'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '100'
        p_str += ', '
        p_str += 'large '  + '65-70' +' %'
        p_str += ', '
        p_str += 'mid '  + '20' + ' %'
        p_str += ', '
        p_str += 'small '  + '10-15' + ' %'
        p_str += '\n'
        fh.write(p_str)
        fh.close()

    # print(all holdings : plus and zero)
    def plan_dump_sorted_units(self, out_filename):
        self.plan_dump_generic(out_filename, sort_type_rank=False)

    # print(all holdings : plus and zero)
    def plan_dump_all(self, out_filename):
        self.plan_dump_generic(out_filename, sort_type_rank=True)

    # print(plus holdings only)
    def plan_dump_plus(self, out_filename):
        self.plan_dump_generic(out_filename, sort_type_rank=True, plus_holdings=True)

    # print(zero holdings only)
    def plan_dump_zero(self, out_filename):
        self.plan_dump_generic(out_filename, sort_type_rank=True, zero_holdings=True)

    def get_plan_comp_units(self, name):
        if name in self.plan_comp_units:
            return self.plan_comp_units[name]
        else:
            print('invalid key :', name)

    def print_comp_data(self):
        print(self.plan_comp_units)

    def size_comp_data(self):
        print(len(self.plan_comp_units))

    def get_plan_indu_units(self, name):
        if name in self.plan_indu_units:
            return self.plan_indu_units[name]
        else:
            print('invalid key :', name)

    def print_indu_data(self):
        print(self.plan_indu_units)

    def size_indu_data(self):
        print(len(self.plan_indu_units))
