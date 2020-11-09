#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3

import cutil.cutil

from database.database import *


class Nach(Database):
    def __init__(self):
        super(Nach, self).__init__()
        self.nach_aliases = {}
        self.nach_aliases_uc = {}
        self.debug_level = 0
        self.nach_table_truncate = False
        self.nach_table_name = "global_nach"
        self.nach_table_dict = {
            "name": "text",
            "ticker": "text"
        }

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def nach_table_reload(self, truncate=False):
        self.nach_table_truncate = truncate

    def nach_load_row(self, row):
        try:
            if self.debug_level > 1:
                print('row : ', row);

            name_alias, ticker = row
            name_alias = name_alias.strip().upper()
            ticker = ticker.strip().upper()
            if self.debug_level > 1:
                print('alias ', name_alias, 'ticker ', ticker)
            self.nach_aliases[name_alias] = ticker
        except ValueError:
            print('ValueError ', row)
        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def nach_load_data(self, in_filename):
        table = self.nach_table_name

        if self.nach_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_amfi_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.nach_insert_data(in_filename)
        else:
            print('nach data already loaded in db', row_count)
        print('display db data')
        self.nach_load_db()

    def nach_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.nach_table_name, self.nach_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.nach_table_name, self.nach_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            if self.debug_level > 1:
                print(csv_reader)
            # insert row
            cursor.executemany(insert_sql, csv_reader)
            # commit db changes
            self.db_conn.commit()
        print('loaded aliases from', in_filename)

    def nach_load_db(self):
        table = self.nach_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.nach_load_row(row)
        print('loaded aliases count ', len(self.nach_aliases))
        # create an upper case list
        for k, v in self.nach_aliases.items():
            self.nach_aliases_uc[k.upper()] = v.upper()

    def nach_dump_phase1(self, out_filename):
        if self.debug_level > 0:
            print('output filename ', out_filename)
        fh = open(out_filename, "w")
        fh.write('nach_name, nach_ticker\n')
        for name in sorted(self.nach_aliases):
            if self.debug_level > 1:
                print('name : ticker ', name, ':', ticker)
            p_str = name
            p_str += ', '
            p_str += self.nach_aliases[name] 
            p_str += '\n'
            fh.write(p_str);
        fh.close()
