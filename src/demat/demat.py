#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import cutil.cutil

from amfi.amfi import *

class Demat(Amfi):

    def __init__(self):
        super(Demat, self).__init__()
        self.company_name = {}
        self.demat_txn_last_type = {}
        self.demat_txn_buy_qty = {}
        self.demat_txn_buy_price = {}
        self.demat_txn_sale_qty = {}
        self.demat_txn_sale_price = {}
        self.demat_txn_last_date = {}
        self.demat_txn_first_buy_date = {}
        self.demat_txn_list = {}
        self.demat_summary_rw_list = []
        self.demat_summary_qty = {}
        self.demat_summary_acp  = {}
        self.demat_summary_upl_pct = {}
        # stock keeping units : sku
        self.demat_summary_sku = {}
        self.demat_table_truncate = False
        self.debug_level = 0
        self.demat_txn_table_name = "demat_txn"
        self.demat_txn_table_dict = {
            "stock_symbol": "text",
            "company_name": "text",
            "isin_code": "text",
            "action": "text",
            "quantity": "text",
            "txn_price": "text",
            "brokerage": "text",
            "txn_charges": "text",
            "stamp_duty": "text",
            "segment": "text",
            "stt": "text",
            "remarks": "text",
            "txn_date": "text",
            "exchange": "text",
            "unused1": "text"
        }
        self.demat_summary_table_name = "demat_summary"
        self.demat_summary_table_dict = {
            "stock_symbol": "text",
            "company_name": "text",
            "isin_code": "text",
            "qty": "text",
            "acp": "text",
            "cmp": "text",
            "pct_change": "text",
            "value_cost": "text",
            "value_market": "text",
            "realized_pl": "text",
            "unrealized_pl": "text",
            "unrealized_pl_pct": "text",
            "unused1": "text"
        }
        print('init : Demat')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def demat_table_reload(self, truncate=False):
        self.demat_table_truncate = truncate

    def demat_txn_load_row(self, row):
        try:
            row_list = row
            # skip header
            if row_list[0] == 'Stock Symbol':
                return
            else:
                # this is not used as ICICI direct uses different names
                stock_symbol = row_list[0].strip()

            comp_name = row_list[1]
            isin_code   = (row_list[2]).upper().strip()
            stock_symbol = self.amfi_get_value_by_isin(isin_code, "ticker")
            # ignore Gold ETF : Kotak, HDFC etc
            if stock_symbol == 'UNK_TICKER' and comp_name.find("GOLD") == -1:
                print("isin", isin_code, "symbol", stock_symbol, "company", comp_name)

            txn_type = row_list[3]
            txn_qty = row_list[4]
            txn_price = str(int(round(float(row_list[5]))))
            txn_date = row_list[12]

            p_str = stock_symbol
            p_str += ','
            p_str += isin_code
            p_str += ','
            p_str += comp_name
            p_str += ','
            p_str += txn_type
            p_str += ','
            p_str += str(txn_qty)
            p_str += ','
            p_str += txn_price
            p_str += ','
            p_str += txn_date
            p_str += '\n'

            if self.debug_level > 1:
                print(p_str)

            if stock_symbol in self.demat_txn_list:
                self.demat_txn_list[stock_symbol] += p_str
            else:
                self.demat_txn_list[stock_symbol] = p_str

            self.company_name[stock_symbol] = cutil.cutil.normalize_comp_name(comp_name)
            if txn_type == "Buy":
                if stock_symbol in self.demat_txn_buy_qty:
                    self.demat_txn_buy_qty[stock_symbol] += int(txn_qty)
                    self.demat_txn_buy_price[stock_symbol] += int(round(float(txn_price))) * int(txn_qty)
                else:
                    self.demat_txn_buy_qty[stock_symbol] = int(txn_qty)
                    self.demat_txn_buy_price[stock_symbol] = int(round(float(txn_price))) * int(txn_qty)
            else:
                if stock_symbol in self.demat_txn_sale_qty:
                    self.demat_txn_sale_qty[stock_symbol] += int(txn_qty)
                    self.demat_txn_sale_price[stock_symbol] += int(round(float(txn_price))) * int(txn_qty)
                else:
                    self.demat_txn_sale_qty[stock_symbol] = int(txn_qty)
                    self.demat_txn_sale_price[stock_symbol] = int(round(float(txn_price))) * int(txn_qty)

            # skip updating bonus entries
            if txn_price != 0:
                self.demat_txn_last_type[stock_symbol] = txn_type
                self.demat_txn_last_date[stock_symbol] = txn_date
                if txn_type == "Buy":
                    if stock_symbol not in self.demat_txn_first_buy_date:
                        self.demat_txn_first_buy_date[stock_symbol] = txn_date
                if txn_type == "Sell":
                    # ignore previous buy entries
                    # assume - last SELL to be full sale.
                    del self.demat_txn_first_buy_date[stock_symbol]
        except KeyError:
            print("demat key error:", sys.exc_info())
            traceback.print_exc()
        except:
            print("demat unexpected error:", sys.exc_info())
            traceback.print_exc()


    def demat_summary_load_row(self, row):
        try:
            row_list = row
            # skip header : sometime Stock Symbol appears as 'tock Symbol'
            if row_list[0] == 'Stock Symbol' or row_list[1] == 'Company Name':
                return

            # not used
            # stock_symbol = row_list[0]
            comp_name = row_list[1]
            isin_code = (row_list[2]).upper().strip()
            stock_symbol = self.amfi_get_value_by_isin(isin_code, "ticker")
            self.demat_summary_rw_list.append(stock_symbol)
            qty = row_list[3]
            acp = row_list[4]
            cmp = row_list[5]
            pct_change = row_list[6]
            value_cost = row_list[7]
            value_market = row_list[8]
            realized_pl = row_list[9]
            unrealized_pl = row_list[10]
            unrealized_pl_pct = row_list[11]
            unused1 = row_list[12]
            self.demat_summary_qty[stock_symbol] = qty
            self.demat_summary_acp[stock_symbol] = acp
            self.demat_summary_upl_pct[stock_symbol] = unrealized_pl_pct
            if int(qty) > 0:
                sku = int(round(float(qty) * float(acp) / 1000))
                if self.debug_level > 1:
                    print(stock_symbol, "qty", qty, "acp", acp, "sku", sku)
            else:
                if self.debug_level > 0:
                    print("unexpected: qty 0")
                sku = 0
            # store
            self.demat_summary_sku[stock_symbol] = sku
        except:
            print("demat_summary_load_row Unexpected error:", sys.exc_info(), row)

    def demat_txn_load_data(self, in_filename):
        table = "demat_txn"
        if self.demat_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.demat_txn_insert_data(in_filename)
        else:
            print('demat_txn data already loaded in db', row_count)
        print('display db data')
        self.demat_txn_load_db()


    def demat_summary_load_data(self, in_filename):
        table = "demat_summary"
        if self.demat_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.demat_summary_insert_data(in_filename)
        else:
            print('demat_summary data already loaded in db', row_count)
        print('display db data')
        self.demat_summary_load_db()

    def demat_txn_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.demat_txn_table_name, self.demat_txn_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.demat_txn_table_name, self.demat_txn_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(insert_sql, csv_reader)
            # commit db changes
            self.db_conn.commit()


    def demat_summary_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.demat_summary_table_name, self.demat_summary_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.demat_summary_table_name, self.demat_summary_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            # insert row
            cursor.executemany(insert_sql, csv_reader)
            # commit db changes
            self.db_conn.commit()

    def demat_txn_load_db(self):
        table = "demat_txn"
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1 :
                print(row)
            self.demat_txn_load_row(row)
        # self.demat_txn_prepare_data()


    def demat_summary_load_db(self):
        table = "demat_summary"
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1 :
                print(row)
            self.demat_summary_load_row(row)
        # self.prepare_demat_data()

    def demat_dump_txn_detailed(self, out_filename):
        fh = open(out_filename, "w")
        fh.write('stock_symbol, isin_code, comp_name, action, qty, price, txn_date\n')
        for stock_symbol in sorted(self.demat_txn_list):
            if self.debug_level > 1:
                print('dumping stock', stock_symbol)
            fh.write(self.demat_txn_list[stock_symbol])
        fh.close()

    def demat_dump_txn_compressed(self, out_filename):
        fh = open(out_filename, "w")
        fh.write(
            'stock_symbol, isin_code, comp_name, buy_qty, sale_qty, buy_price, sale_price, demat_txn_last_type, demat_txn_last_date\n')
        for stock_symbol in sorted(self.demat_txn_list):
            if stock_symbol == 'Stock Symbol':
                continue
            isin_code = self.amfi_get_value_by_ticker(stock_symbol, "isin")
            p_str = stock_symbol
            p_str += ','
            p_str += isin_code 
            p_str += ','
            p_str += self.company_name[stock_symbol]
            p_str += ','
            p_str += str(self.demat_txn_buy_qty[stock_symbol])
            p_str += ','
            if stock_symbol in self.demat_txn_sale_qty:
                p_str += str(self.demat_txn_sale_qty[stock_symbol])
            else:
                p_str += '0'
            p_str += ','
            p_str += str(self.demat_txn_buy_price[stock_symbol])
            p_str += ','
            if stock_symbol in self.demat_txn_sale_price:
                p_str += str(self.demat_txn_sale_price[stock_symbol])
            else:
                p_str += '0'
            p_str += ','
            p_str += self.demat_txn_last_type[stock_symbol]
            p_str += ','
            p_str += self.demat_txn_last_date[stock_symbol]
            p_str += '\n'
            fh.write(p_str)
        fh.close()

    def demat_dump_txn_summary(self, out_filename, positive_holdings=None):

        # print(self.demat_summary_sku)

        fh = open(out_filename,"w")
        fh.write(
            'stock_symbol, isin_code, comp_name, demat_summary_qty, demat_summary_acp, demat_summary_sku, demat_txn_last_type, demat_txn_last_date\n')
        for stock_symbol in sorted(self.demat_txn_list):
            if stock_symbol == 'Stock Symbol':
                continue
            isin_code = self.amfi_get_value_by_ticker(stock_symbol, "isin")
            p_str = stock_symbol 
            p_str += ','
            p_str += isin_code
            p_str += ','
            p_str += self.company_name[stock_symbol]
            p_str += ','
            p_str += str(self.demat_summary_qty[stock_symbol])
            p_str += ','
            p_str += str(self.demat_summary_acp[stock_symbol])
            p_str += ','
            if stock_symbol in self.demat_summary_sku:
                p_str += str(self.demat_summary_sku[stock_symbol])
            else:
                p_str += '0'
                # print(":",stock_symbol,":")
            p_str += ','
            p_str += self.demat_txn_last_type[stock_symbol]
            p_str += ','
            p_str += self.demat_txn_last_date[stock_symbol]
            p_str += '\n'
            if positive_holdings:
                if int(self.demat_summary_qty[stock_symbol]) > 0:
                    fh.write(p_str)
            else:
                fh.write(p_str)
        fh.close()

    def demat_dump_summary_ticker_only(self, out_filename):
        fh = open(out_filename, "w")
        for stock_symbol in sorted(self.demat_summary_rw_list):
            p_str = stock_symbol
            p_str += '\n'
            if stock_symbol == 'Stock Symbol':
                continue
            if int(self.demat_summary_qty[stock_symbol]) > 0:
                fh.write(p_str)
            else:
                if self.debug_level > 0:
                    print('stock qty 0', stock_symbol)
        fh.close()

    def demat_summary_get_upl_pct_by_ticker(self, ticker):
        if ticker in self.demat_summary_upl_pct:
            return self.demat_summary_upl_pct[ticker]
        return 0

    def demat_summary_get_acp_by_ticker(self, ticker):
        if ticker in self.demat_summary_acp:
            return self.demat_summary_acp[ticker]
        return 0

    def demat_summary_get_qty_by_ticker(self, ticker):
        if ticker in self.demat_summary_qty:
            return self.demat_summary_qty[ticker]
        return 0

    def demat_summary_get_holding_value(self, ticker):
        return self.demat_summary_get_qty_by_ticker(ticker) * self.demat_summary_get_acp_by_ticker(ticker)

    def demat_summary_get_units_by_ticker(self, ticker):
        if ticker in self.demat_summary_sku:
            return self.demat_summary_sku[ticker]
        return 0

    def demat_txn_get_last_date_by_ticker(self, ticker):
        if ticker in self.demat_txn_last_date:
            return self.demat_txn_last_date[ticker]
        return '-'

    def demat_txn_get_first_buy_date_by_ticker(self, ticker):
        if ticker in self.demat_txn_first_buy_date:
            return self.demat_txn_first_buy_date[ticker]
        return '-'

    def demat_txn_get_last_type_by_ticker(self, ticker):
        if ticker in self.demat_txn_last_type:
            return self.demat_txn_last_type[ticker]
        return '-'
