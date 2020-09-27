#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import sqlite3

import logging

import traceback

import argparse

import cutil.cutil

from prettytable import PrettyTable

from database.database import *

class Amfi(Database):
    def __init__(self):
        super(Amfi, self).__init__()
        # isin number
        self.amfi_isin_list = []
        self.amfi_ticker_list = []
        self.amfi_captype_list = []
        # serial number
        self.amfi_cname = {}
        self.amfi_mcap = {}
        self.amfi_rank = {}
        self.amfi_captype = {}
        self.amfi_ticker_isin_dict = {}
        self.amfi_isin_ticker_dict = {}
        self.debug_level = 0
        self.amfi_table_truncate = False
        self.amfi_table_name = "global_amfi"
        self.amfi_table_dict = {
            "comp_rank": "int",
            "comp_name": "text",
            "comp_isin": "text",
            "bse_symbol": "text",
            "nse_symbol": "text",
            "avg_mcap": "text",
            "cap_type": "text",
        }

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def amfi_table_reload(self, truncate=False):
        self.amfi_table_truncate = truncate

    def amfi_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                logging.info('ignored empty row %s', row_list)
                return

            comp_rank = row_list[0]
            if comp_rank == 'Sr. No.' or comp_rank == "sr_no":
                logging.info('skipped header line %s', row_list)
                return

            # mysql - automatically number
            if self.config_db_type != 'mariadb':
                comp_rank = cutil.cutil.get_number(comp_rank)

            comp_name = row_list[1]
            isin_number = row_list[2]
            bse_ticker = row_list[3].upper().strip()
            nse_ticker = row_list[4]
            if self.config_db_type == 'mariadb':
                avg_mcap = row_list[5]
            else:
                avg_mcap = cutil.cutil.get_number(row_list[5])
            captype = row_list[6].strip()

            comp_name = cutil.cutil.normalize_comp_name(comp_name)

            logging.debug('comp_rank : %s isin_number: %s bse_ticker : %s nse_ticker : %s avg_mcap : %s captype : %s'
                          'comp_name : %s', comp_rank, isin_number, bse_ticker, nse_ticker, avg_mcap, captype,
                          comp_name)

            if nse_ticker == '':
                if bse_ticker != '':
                    self.amfi_rank[bse_ticker] = comp_rank
                    self.amfi_ticker_isin_dict[bse_ticker] = isin_number
                    self.amfi_isin_ticker_dict[isin_number] = nse_ticker
                    self.amfi_cname[bse_ticker] = comp_name
                    self.amfi_mcap[bse_ticker] = avg_mcap
                    self.amfi_captype[bse_ticker] = captype
                    self.amfi_isin_list.append(isin_number)
                    self.amfi_ticker_list.append(bse_ticker)
            else:
                self.amfi_rank[nse_ticker] = comp_rank
                self.amfi_ticker_isin_dict[nse_ticker] = isin_number
                self.amfi_isin_ticker_dict[isin_number] = nse_ticker
                self.amfi_cname[nse_ticker] = comp_name
                self.amfi_mcap[nse_ticker] = avg_mcap
                self.amfi_captype[nse_ticker] = captype
                self.amfi_isin_list.append(isin_number)
                self.amfi_ticker_list.append(nse_ticker)

            if captype not in self.amfi_captype_list:
                self.amfi_captype_list.append(captype)

            logging.debug('comp_name : %s isin_number: %s', comp_name, isin_number)

        except IndexError:
            logging.error('except %s', row)
        except:
            logging.error('except %s', row)
            traceback.print_exc()

    def amfi_store_data_to_db(self, in_filename):
        table = self.amfi_table_name

        if self.amfi_table_truncate:
            self.db_table_truncate(table)

        # row_count = self.count_amfi_db(table)
        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.amfi_insert_data(in_filename)
        else:
            logging.info('amfi data already loaded in db %d', row_count)

    def amfi_get_insert_row(self, line, row_bank):

        # split on comma
        line = re.sub(',",', ',', line)
        line = re.sub('"', '', line)
        row_list = line.split(',')

        logging.debug('row_list %s', row_list)
        logging.debug('len row_list %d', len(row_list))

        (comp_rank, comp_name, comp_isin, bse_symbol, nse_symbol, avg_mcap, cap_type) = row_list

        # remove new line character from end
        cap_type = cap_type.strip('\n')

        if comp_rank == 'Sr. No.' or comp_rank == "sr_no":
            logging.info('skipped header line %s', row_list)
            logging.info('len row_list %d', len(row_list))
            return

        # remove any un-required stuff
        new_row = (comp_rank, comp_name, comp_isin, bse_symbol, nse_symbol, avg_mcap, cap_type)
        row_bank.append(new_row)

    def amfi_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.amfi_table_name, self.amfi_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.amfi_table_name, self.amfi_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            # insert row
            row_bank = []
            for line in csvfile:
                self.amfi_get_insert_row(line, row_bank)
            logging.info('loaded entries %s', len(row_bank))
            logging.info('from %s', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def amfi_load_data_from_db(self):
        table = self.amfi_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug('%s', row)
            self.amfi_load_row(row)

    def amfi_dump(self, pretty_dump, out_filename):

        logging.info('output filename %s', out_filename)

        pt = PrettyTable()
        pt.field_names = ["amfi_rank", "amfi_cname", "amfi_isin", "amfi_ticker", "amfi_mcap", "amfi_captype"]

        fh = open(out_filename, "w")

        dump_first_rec = True
        for ticker in sorted(self.amfi_rank, key=self.amfi_rank.__getitem__):
            if dump_first_rec:
                dump_first_rec = False
                logging.debug('ticker  %s', ticker)

            row_list = [str(self.amfi_rank[ticker])]
            row_list.append(self.amfi_cname[ticker])
            row_list.append(self.amfi_ticker_isin_dict[ticker])
            row_list.append(ticker)
            row_list.append(str(self.amfi_mcap[ticker]))
            row_list.append(self.amfi_captype[ticker])

            pt.add_row(row_list)

        if pretty_dump:
            fh.write(str(pt))
            fh.close()

    def amfi_export(self, export_to_file, out_filename):

        logging.info('output filename %s', out_filename)

        field_names = ["amfi_rank", "amfi_cname", "amfi_isin", "amfi_ticker", "amfi_mcap", "amfi_captype"]

        if export_to_file:
            fh = open(out_filename, "w")
            p_hdr = ','.join(field_names)
            p_hdr += '\n'
            fh.write(p_hdr)

        dump_first_rec = True
        for ticker in sorted(self.amfi_rank, key=self.amfi_rank.__getitem__):
            if dump_first_rec:
                logging.debug('ticker  %s', ticker)
                dump_first_rec = False

            row_list = [str(self.amfi_rank[ticker])]
            row_list.append(self.amfi_cname[ticker])
            row_list.append(self.amfi_ticker_isin_dict[ticker])
            row_list.append(ticker)
            row_list.append(str(self.amfi_mcap[ticker]))
            row_list.append(self.amfi_captype[ticker])

            p_str = ','.join(row_list)
            p_str += '\n'

            if export_to_file:
                fh.write(p_str);

        if export_to_file:
            fh.close()

    def amfi_get_ticker_by_name(self, req_name):
        req_name = re.sub('\s+', ' ', req_name).strip()
        for amfi_ticker in sorted(self.amfi_cname):
            # try to find a matching company
            comp_name = self.amfi_cname[amfi_ticker]
            comp_name = comp_name.strip()
            if re.match(req_name, comp_name) or req_name.upper() == amfi_ticker:
                logging.debug('found match : name : %s', req_name)
                return amfi_ticker

        logging.debug('amfi : comp not found : req_name : %s', req_name)
        return ''

    def amfi_get_value_by_isin(self, isin, value_name):
        # return ticker
        if value_name == "ticker":
            return self.amfi_get_ticker_by_isin(isin)
        try:
            ticker = self.amfi_isin_ticker_dict[isin]
            if ticker:
                self.amfi_get_value_by_ticker(self, isin, value_name)
        except KeyError:
            logging.error('KeyError ', isin)
            traceback.print_exc()
        return 'UNK_COMP_2'

    def amfi_get_value_by_ticker(self, ticker, value_name):
        try:
            if ticker:
                if ticker == 'UNK_TICKER':
                    return 'UNK'
                if value_name == "cname":
                    if ticker in self.amfi_cname:
                        return self.amfi_cname[ticker]
                    else:
                        return 'UNK_cname'
                if value_name == "mcap":
                    if ticker in self.amfi_mcap:
                        return self.amfi_mcap[ticker]
                    else:
                        return 0
                if value_name == "rank":
                    if ticker in self.amfi_rank:
                        return self.amfi_rank[ticker]
                    else:
                        return 0
                if value_name == "captype":
                    if ticker in self.amfi_captype:
                        return self.amfi_captype[ticker]
                    else:
                        return 'UNK_captype'
                if value_name == "isin":
                    return self.amfi_get_isin_by_ticker(ticker)
        except KeyError:
            print('KeyError ', ticker)
            traceback.print_exc()
        except:
            print('Except ', ticker)
            traceback.print_exc()
        if value_name == "mcap" or value_name == "rank":
            return 0
        else:
            return 'UNK_COMP_E'

    def amfi_get_ticker_by_isin(self, amfi_isin):
        if amfi_isin in self.amfi_isin_list:
            return self.amfi_isin_ticker_dict[amfi_isin]
        return 'UNK_TICKER'

    def amfi_get_isin_by_ticker(self, ticker):
        try:
            if ticker in self.amfi_ticker_isin_dict:
                amfi_isin = self.amfi_ticker_isin_dict[ticker]
                return amfi_isin
        except KeyError:
            print('KeyError ', ticker)
            traceback.print_exc()
        return 'UNK_ISIN'


if __name__ == "__main__":

    def main():
        print('in main')

        parser = argparse.ArgumentParser(description='Process arguments')
        # dest= not required as option itself is the destination in args
        parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int,
                            choices=[0, 1, 2, 3])
        parser.add_argument('-t', '--truncate_table', default='False', help='specify to truncate', action='store_true')
        parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
        parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')
        parser.add_argument('-s', '--save_to_db', default='True', help='save data to db', action='store_true')
        parser.add_argument('-x', '--export_to_file', default='True', help='export data to file', action='store_true')
        parser.add_argument('-p', '--pretty_dump', default='True', help='pretty dump', action='store_true')
        args = parser.parse_args()

        log_level = args.log_level
        truncate_table = args.truncate_table
        save_to_db = args.save_to_db
        export_to_file = args.export_to_file
        pretty_dump = args.pretty_dump

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

        # Main caller
        program_name = sys.argv[0]

        if len(sys.argv) < 4:
            print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> ... ")
            sys.exit(1)

        print('args :', len(sys.argv))

        amfi = Amfi()

        amfi.set_log_level(log_level)

        if truncate_table:
            amfi.amfi_table_reload(truncate_table)

        if save_to_db:
            amfi.amfi_store_data_to_db(in_filename_phase[0])

        amfi.amfi_load_data_from_db()

        amfi.amfi_export(export_to_file, out_filename_phase[0])

        amfi.amfi_dump(pretty_dump, out_filename_phase[1])

        print('end of main')


    main()
