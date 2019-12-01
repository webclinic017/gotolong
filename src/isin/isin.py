#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import cutil.cutil

from database.database import *

class Isin(Database):
    def __init__(self):
        super(Isin, self).__init__()
        self.isin_table_name = "isin"
        self.isin_table_columns = ["company_name", "industry_name", "symbol_ticker", "series", "isin_code"]
        self.isin_code_both = []
        self.isin_symbol = {}
        self.isin_name_bse = {}
        self.isin_name_nse = {}
        self.isin_industry_dict = {}
        self.isin_industry_list = []
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

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

            comp_name = cutil.cutil.normalize_comp_name(comp_name)

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
                print('comp_name : ', comp_name , '\n')
                print('isin_code : ', isin_code , '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def isin_load_data(self, in_filename, bse_nse):
        table = "isin"
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.insert_isin_data(in_filename)
        else:
            print('isin data already loaded in db', row_count)
        print('display db data')
        self.isin_load_db()

    def isin_insert_data(self, in_filename):
        table_name = self.isin_table_name
        table_columns = self.isin_table_columns

        insert_sql = "insert into "
        insert_sql += table_name
        insert_sql += "("

        iter = 0
        for column_name in table_columns:
            insert_sql += column_name
            if iter != len(table_columns) - 1:
                insert_sql += ","
            iter += 1

        insert_sql += ") values("

        iter = 0
        for column_name in table_columns:
            insert_sql += ":"
            insert_sql += column_name
            if iter != len(table_columns) - 1:
                insert_sql += ","
            iter += 1
        insert_sql += ")"

        print(insert_sql)

        create_sql = "create table if not exists "
        create_sql += table_name
        create_sql += "("

        iter = 0
        for column_name in table_columns:
            create_sql += column_name
            if iter != len(table_columns) - 1:
                create_sql += " text,"
            iter += 1
        create_sql += " text)"
        print(create_sql)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(insert_sql, csv_reader)
            # commit db changes
            self.db_conn.commit()

    def isin_load_db(self):
        table_name = self.isin_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1 :
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
            if isin_code in  self.isin_symbol:
                ticker_symbol = self.isin_symbol[isin_code]
                if req_name.upper() == ticker_symbol :
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
            if isin_code in  self.isin_symbol:
                ticker_symbol = self.isin_symbol[isin_code]
                if req_name.upper() == ticker_symbol :
                    if self.debug_level > 1:
                        print('found ticker : ', req_name)
                    return isin_code
        if self.debug_level > 1:
            print('demat not found : req_name :',req_name,':')
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
