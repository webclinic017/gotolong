#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import calendar
import logging

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
        self.demat_sum_rw_list = []
        self.demat_sum_qty = {}
        self.demat_sum_acp = {}
        self.demat_sum_upl_pct = {}
        self.demat_sum_captype_stock_count = {}
        self.demat_sum_captype_stock_cost_value = {}
        self.demat_sum_captype_stock_market_value = {}
        self.demat_sum_captype_unrealized_pl = {}
        # stock keeping units : sku
        self.demat_sum_sku = {}
        self.demat_table_truncate = False
        self.demat_lc_weight = self.config_lc_weight
        self.demat_mc_weight = self.config_mc_weight
        self.demat_sc_weight = self.config_sc_weight
        self.demat_abbr_to_num_dict = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        self.debug_level = 0
        self.demat_txn_table_name = "user_demat_txn"
        self.demat_txn_table_dict = {
            "stock_symbol": "text",
            "comp_name": "text",
            "isin_code": "text",
            "action": "text",
            "quantity": "int",
            "txn_price": "float",
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
        self.demat_sum_table_name = "user_demat_sum"
        self.demat_sum_table_dict = {
            "stock_symbol": "text",
            "comp_name": "text",
            "isin_code_id": "text",
            "qty": "int",
            "acp": "float",
            "cmp": "text",
            "pct_change": "text",
            "value_cost": "float",
            "value_market": "float",
            "days_gain": "text",
            "days_gain_pct": "text",
            "realized_pl": "text",
            "unrealized_pl": "text",
            "unrealized_pl_pct": "text",
            "unused1": "text"
        }
        self.demat_printed_ignored_isin = {}

        logging.info('init : Demat')

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

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
                if isin_code not in self.demat_printed_ignored_isin:
                    self.demat_printed_ignored_isin[isin_code] = 'yes'
                    logging.info("isin", isin_code, "symbol", stock_symbol, "company", comp_name)

            txn_type = row_list[3]
            txn_qty = row_list[4]
            txn_price = str(int(round(float(row_list[5]))))
            # convert datetime.date to str
            txn_date = str(row_list[12])

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

            logging.debug('%s', p_str)

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
                    if stock_symbol in self.demat_txn_first_buy_date:
                        del self.demat_txn_first_buy_date[stock_symbol]
        except KeyError:
            logging.error("demat key error:", sys.exc_info())
            traceback.print_exc()
        except:
            logging.error("demat unexpected error:", sys.exc_info())
            traceback.print_exc()

    def demat_sum_load_row(self, row):
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
            self.demat_sum_rw_list.append(stock_symbol)
            qty = row_list[3]
            acp = row_list[4]
            cmp = row_list[5]
            pct_change = row_list[6]
            value_cost = row_list[7]
            value_market = row_list[8]
            days_gain = row_list[9]
            days_gain_pct = row_list[10]
            realized_pl = row_list[11]
            unrealized_pl = row_list[12]
            unrealized_pl_pct = row_list[13]
            unused1 = row_list[14]
            self.demat_sum_qty[stock_symbol] = qty
            self.demat_sum_acp[stock_symbol] = acp
            self.demat_sum_upl_pct[stock_symbol] = unrealized_pl_pct
            if int(qty) > 0:
                sku = int(round(float(qty) * float(acp) / 1000))
                logging.debug(stock_symbol, "qty", qty, "acp", acp, "sku", sku)
            else:
                logging.debug("unexpected: qty 0")
                sku = 0
            # store
            self.demat_sum_sku[stock_symbol] = sku

            captype = self.amfi_get_value_by_ticker(stock_symbol, "captype")

            if captype in self.demat_sum_captype_stock_count:
                self.demat_sum_captype_stock_count[captype] += 1
            else:
                self.demat_sum_captype_stock_count[captype] = 1

            if captype in self.demat_sum_captype_stock_cost_value:
                self.demat_sum_captype_stock_cost_value[captype] += round(float(value_cost))
            else:
                self.demat_sum_captype_stock_cost_value[captype] = round(float(value_cost))

            if captype in self.demat_sum_captype_stock_market_value:
                self.demat_sum_captype_stock_market_value[captype] += round(float(value_market))
            else:
                self.demat_sum_captype_stock_market_value[captype] = round(float(value_market))

            if captype in self.demat_sum_captype_unrealized_pl:
                self.demat_sum_captype_unrealized_pl[captype] += round(float(unrealized_pl))
            else:
                self.demat_sum_captype_unrealized_pl[captype] = round(float(unrealized_pl))

        except:
            logging.error("demat_sum_load_row Unexpected error:", sys.exc_info(), row)

    def demat_txn_load_data(self, in_filename):
        table = self.demat_txn_table_name
        if self.demat_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.demat_txn_insert_data(in_filename)
        else:
            logging.info('demat_txn data already loaded in db', row_count)
        logging.info('display db data')
        self.demat_txn_load_db()

    def demat_sum_load_data(self, in_filename):
        table = self.demat_sum_table_name
        if self.demat_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.demat_sum_insert_data(in_filename)
        else:
            logging.info('demat_sum data already loaded in db', row_count)
        logging.info('display db data')
        self.demat_sum_load_db()

    def demat_txn_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        logging.debug('row_list', row_list)
        logging.debug('len row_list', len(row_list))

        (stock_symbol, comp_name, isin_code, txn_type, txn_qty, txn_price, brokerage, txn_charges, stamp_duty, segment,
         stt, remarks, txn_date, exchange, unused1) = row_list

        logging.debug('stock symbol', stock_symbol)

        # bypass header
        if stock_symbol.strip() == 'Stock Symbol':
            logging.info('bypassed header line', row_list)
            return

        try:
            # dd-mmm-yy
            txn_date_arr = txn_date.split('-')
            txn_day = txn_date_arr[0].strip()
            txn_month = txn_date_arr[1].strip()
            txn_year = txn_date_arr[2].strip()
            if txn_month.isdigit():
                # get rid of leading 0 in month number
                txn_month = str(int(txn_month))
            else:
                # month name to number
                txn_month = str(self.demat_abbr_to_num_dict[txn_month])
            txn_date_iso = txn_year + "-" + txn_month + "-" + txn_day
            # ignore rest
        except ValueError:
            logging.error('ValueError ', txn_date, row_list)
        except IndexError:
            logging.error('IndexError ', txn_date, row_list)

        new_row = (
        stock_symbol, comp_name, isin_code, txn_type, txn_qty, txn_price, brokerage, txn_charges, stamp_duty, segment,
        stt, remarks, txn_date_iso, exchange, unused1)
        row_bank.append(new_row)

    def demat_txn_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.demat_txn_table_name, self.demat_txn_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.demat_txn_table_name, self.demat_txn_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            row_bank = []
            for line in csvfile:
                self.demat_txn_get_insert_row(line, row_bank)
            logging.info('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def demat_sum_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        (stock_symbol, comp_name, isin_code_id, qty, acp, cmp, pct_change, value_cost, value_market, \
         days_gain, days_gain_pct, realized_pl, unrealized_pl, unrealzied_pl_pct, unused1) = row_list

        logging.debug('row_list', row_list)
        logging.debug('len row_list', len(row_list))

        # bypass header
        if stock_symbol.strip() == 'Stock Symbol':
            logging.info('bypassed header line', row_list)
            return

        new_row = (stock_symbol, comp_name, isin_code_id, qty, acp, cmp, pct_change, value_cost, value_market, \
                   days_gain, days_gain_pct, realized_pl, unrealized_pl, unrealzied_pl_pct, unused1)
        row_bank.append(new_row)

    def demat_sum_insert_data(self, in_filename):

        create_sql = cutil.cutil.get_create_sql(self.demat_sum_table_name, self.demat_sum_table_dict)
        insert_sql = cutil.cutil.get_insert_sql(self.demat_sum_table_name, self.demat_sum_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            row_bank = []
            for line in csvfile:
                self.demat_sum_get_insert_row(line, row_bank)
            logging.info('loaded entries', len(row_bank), 'from', in_filename)
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def demat_txn_load_db(self):
        table = self.demat_txn_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug(row)
            self.demat_txn_load_row(row)
        # self.demat_txn_prepare_data()

    def demat_sum_load_db(self):
        table = self.demat_sum_table_name
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            logging.debug(row)
            self.demat_sum_load_row(row)
        # self.prepare_demat_data()

    def demat_dump_txn_detailed(self, out_filename):
        fh = open(out_filename, "w")
        fh.write('stock_symbol, isin_code, comp_name, action, qty, price, txn_date\n')
        for stock_symbol in sorted(self.demat_txn_list):
            logging.debug('dumping stock', stock_symbol)
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

        # print(self.demat_sum_sku)

        fh = open(out_filename,"w")
        fh.write(
            'stock_symbol, isin_code, comp_name, demat_sum_qty, demat_sum_acp, demat_sum_sku, demat_txn_last_type, demat_txn_last_date\n')
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
            p_str += str(self.demat_sum_qty[stock_symbol])
            p_str += ','
            p_str += str(self.demat_sum_acp[stock_symbol])
            p_str += ','
            if stock_symbol in self.demat_sum_sku:
                p_str += str(self.demat_sum_sku[stock_symbol])
            else:
                p_str += '0'
                # print(":",stock_symbol,":")
            p_str += ','
            p_str += self.demat_txn_last_type[stock_symbol]
            p_str += ','
            p_str += self.demat_txn_last_date[stock_symbol]
            p_str += '\n'
            if positive_holdings:
                if int(self.demat_sum_qty[stock_symbol]) > 0:
                    fh.write(p_str)
            else:
                fh.write(p_str)
        fh.close()

    def demat_dump_summary_ticker_only(self, out_filename):
        fh = open(out_filename, "w")
        for stock_symbol in sorted(self.demat_sum_rw_list):
            p_str = stock_symbol
            p_str += '\n'
            if stock_symbol == 'Stock Symbol':
                continue
            if int(self.demat_sum_qty[stock_symbol]) > 0:
                fh.write(p_str)
            else:
                logging.debug('stock qty 0', stock_symbol)
        fh.close()

    def demat_dump_summary_captype(self, out_filename):
        fh = open(out_filename, "w")
        fh.write("captype, stocks, cost value, market value, unrealized pl\n")
        for captype in sorted(self.amfi_captype_list):
            p_str = captype
            p_str += ','
            p_str += str(self.demat_sum_captype_stock_count[captype])
            p_str += ','
            p_str += str(self.demat_sum_captype_stock_cost_value[captype])
            p_str += ','
            p_str += str(self.demat_sum_captype_stock_market_value[captype])
            p_str += ','
            p_str += str(self.demat_sum_captype_unrealized_pl[captype])
            p_str += '\n'
            fh.write(p_str)
        fh.close()

    def demat_dump_holdings_by_rank(self, out_filename):
        fh = open(out_filename, "w")
        fh.write('amfi_rank, amfi_ticker, amfi_cname, plan_sku, cur_sku, tbd_sku\n')
        for ticker in sorted(self.amfi_rank, key=self.amfi_rank.__getitem__):
            rank = self.amfi_rank[ticker]
            p_str = str(rank)
            p_str += ', '
            p_str += ticker
            p_str += ', '
            p_str += self.amfi_cname[ticker]
            p_str += ', '

            if ticker in self.demat_sum_sku:
                cur_sku = self.demat_sum_sku[ticker]
            else:
                cur_sku = 0
                if rank <= 250:
                    logging.info("ticker", ticker, "with rank", rank, " doesn't have holdings")
            # large cap
            if rank <= 100:
                plan_sku = self.demat_lc_weight
                # mid cap
            elif rank <= 250:
                plan_sku = self.demat_mc_weight
                # small cap
            else:
                plan_sku = self.demat_sc_weight 

            tbd_sku = plan_sku - cur_sku

            p_str += str(plan_sku)
            p_str += ', '
            p_str += str(cur_sku)
            p_str += ', '
            if tbd_sku > 0:
                p_str += str(tbd_sku)
            else:
                p_str += str(0)

            p_str += '\n'

            # skip dumping unless you hold it after rank 250
            if rank <= 250 or cur_sku > 0:
                fh.write(p_str)
        fh.close()

    def demat_sum_get_upl_pct_by_ticker(self, ticker):
        if ticker in self.demat_sum_upl_pct:
            return self.demat_sum_upl_pct[ticker]
        return 0

    def demat_sum_get_acp_by_ticker(self, ticker):
        if ticker in self.demat_sum_acp:
            return self.demat_sum_acp[ticker]
        return 0

    def demat_sum_get_qty_by_ticker(self, ticker):
        if ticker in self.demat_sum_qty:
            return self.demat_sum_qty[ticker]
        return 0

    def demat_sum_get_holding_value(self, ticker):
        return self.demat_sum_get_qty_by_ticker(ticker) * self.demat_sum_get_acp_by_ticker(ticker)

    def demat_sum_get_units_by_ticker(self, ticker):
        if ticker in self.demat_sum_sku:
            return self.demat_sum_sku[ticker]
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


if __name__ == "__main__":

    def main():
        print('in main')

        parser = argparse.ArgumentParser(description='Process arguments')
        # dest= not required as option itself is the destination in args
        parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int,
                            choices=[0, 1, 2, 3])
        parser.add_argument('-t', '--truncate_table', default='False', help='truncate table', action='store_true')
        parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
        parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

        args = parser.parse_args()

        log_level = args.log_level
        debug_level = args.debug_level
        truncate_table = args.truncate_table

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

        txn_file = in_filename_phase[0]
        summary_file = in_filename_phase[1]

        if debug_level > 1:
            print('args :', len(sys.argv))

        demat = Demat()

        demat.set_log_level(log_level)
        demat.set_debug_level(debug_level)

        if truncate_table:
            demat.demat_table_reload(truncate_table)

        demat.amfi_load_data_from_db()
        demat.demat_txn_load_data(txn_file)
        demat.demat_sum_load_data(summary_file)
        demat.demat_dump_txn_detailed(out_filename_phase[0])
        demat.demat_dump_txn_compressed(out_filename_phase[1])
        demat.demat_dump_txn_summary(out_filename_phase[2])
        # positive holdings
        demat.demat_dump_txn_summary(out_filename_phase[3], True)
        demat.demat_dump_summary_ticker_only(out_filename_phase[4])
        demat.demat_dump_summary_captype(out_filename_phase[5])
        demat.demat_dump_holdings_by_rank(out_filename_phase[6])


    # execute only if run as a script
    main()
