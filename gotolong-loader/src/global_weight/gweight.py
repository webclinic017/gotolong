#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import cutil.cutil

from database.database import *


class Gweight(Database):
    def __init__(self):
        super(Gweight, self).__init__()
        self.gweight_captype_dict = {}
        self.gweight_table_truncate = False
        self.gweight_table_name = "global_weight"
        self.gweight_table_dict = {
            "cap_type": "text",
            "cap_weight": "int"
        }
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def gweight_table_reload(self, truncate=False):
        self.gweight_table_truncate = truncate

    def gweight_table_create(self):
        # dump the sql for creation of table
        create_sql = cutil.cutil.get_create_sql(self.gweight_table_name, self.gweight_table_dict)
        if self.debug_level > 0:
            print(create_sql)

    def gweight_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            cap_type = row_list[0]
            cap_weight = row_list[1]

            self.gweight_captype_dict[cap_type] = cap_weight

            if self.debug_level > 1:
                print('cop_type : ', cap_type, '\n')
                print('cap_weight : ', cap_weight, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def gweight_load_data(self, in_filename):
        table = self.gweight_table_name

        if self.gweight_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.gweight_insert_data(in_filename)
        else:
            print('gweight data already loaded in db', row_count)
        print('display db data')
        self.gweight_load_db()

    def gweight_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        if self.debug_level > 1:
            print('row_list', row_list)
            print('len row_list', len(row_list))

        (cap_type, cap_weight) = row_list

        if cap_type == 'Cap Type' or cap_weight == "Cap Weight":
            if self.debug_level > 0:
                print('skipped header line', row_list)
            return

        # remove any un-required stuff
        new_row = (cap_type, cap_weight)
        row_bank.append(new_row)

    def gweight_insert_data(self, in_filename):
        insert_sql = cutil.cutil.get_insert_sql(self.gweight_table_name, self.gweight_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # insert row
            row_bank = []
            for line in csvfile:
                self.gweight_get_insert_row(line, row_bank)
            print('loaded gweight : ', len(row_bank))
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def gweight_load_db(self):
        table_name = self.gweight_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.gweight_load_row(row)

    def gweight_dump_report_full(self, out_filename):

        fh = open(out_filename, "w")
        fh.write('cap_type, cap_weight\n')
        for cap_type, cap_weight in self.gweight_captype_dict.items():
            p_str = str(cap_type)
            p_str += ', '
            p_str += str(cap_weight)
            p_str += '\n'
            fh.write(p_str);
        fh.close()
