# !/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from datetime import datetime, date


from amfi.amfi import *
from isin.isin import *
from screener.screener import *
from trendlyne.trendlyne import *
from demat.demat import *

from weight.weight import *


class Phealth(Screener, Trendlyne, Demat, Weight):

    def __init__(self):
        super(Phealth, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.phealth_values = {}
        self.debug_level = 0
        print('init : phealth')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def phealth_dump_report(self, out_filename, out_filename_2):

        bat_missing_list = []

        delimit = "\t"
        fh = open(out_filename, "w")

        # oku - one k units
        if delimit == "\t":
            p_str = "ticker\tindustry\tbat\tcmp\tlow_52w\thigh_52w\tup_52w_low\tmos\ttxn_gap\tplan_oku\tcur_oku\ttbd_oku"
        else:
            p_str = "ticker,industry,bat,cmp,low_52w,high_52w,up_52w_low,mos,txn_gap,plan_oku,cur_oku,tbd_oku"

        p_str += '\n'
        phealth_list = ["price", "low52", "high52"]

        fh.write(p_str)

        print(len(self.sc_nsecode))

        iter1 = 2
        for ticker in sorted(self.sc_nsecode):
            try:
                # upper case
                if self.sc_ratio_values[ticker, "reco_type"] == "BUY":

                    p_str = ticker
                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    isin_code = self.amfi_get_value_by_ticker(ticker, "isin")

                    if isin_code in self.isin_industry_dict:
                        industry_name = self.isin_industry_dict[isin_code]
                        p_str += industry_name
                        if self.phealth_values.get((industry_name, "ticker_list")):
                            self.phealth_values[industry_name, "ticker_list"].append(ticker)
                        else:
                            self.phealth_values[industry_name, "ticker_list"] = [ticker]
                    else:
                        p_str += '-'

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    if self.tl_ratio_values.get((ticker, "bat")):
                        p_str += self.tl_ratio_values[ticker, "bat"]
                    else:
                        p_str += '-'
                        bat_missing_list.append(ticker)

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    for phealth_name in phealth_list:
                        # p_str += "'"
                        p_str += '=ROUND(GOOGLEFINANCE(CONCATENATE("NSE:",A'
                        p_str += str(iter1)
                        p_str += '),"'
                        p_str += phealth_name
                        p_str += '"))'
                        # p_str += "'"
                        if delimit == '\t':
                            p_str += '\t'
                        else:
                            p_str += ','

                    p_str += '=IFERROR(ROUND((D'
                    p_str += str(iter1)
                    p_str += '-E'
                    p_str += str(iter1)
                    p_str += ')*100/E'
                    p_str += str(iter1)
                    p_str += '),'
                    p_str += '"-")'

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    p_str += '=IFERROR(ROUND((C'
                    p_str += str(iter1)
                    p_str += '-D'
                    p_str += str(iter1)
                    p_str += ')*100/D'
                    p_str += str(iter1)
                    p_str += '),'
                    p_str += '"-")'

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    # p_str += self.demat_txn_get_last_date_by_ticker(ticker)

                    last_date = self.demat_txn_get_last_date_by_ticker(ticker)

                    old_date_format = "%d-%b-%Y"
                    # new_date_format = '%Y-%m-%d'
                    if last_date != '-':
                        someday = datetime.datetime.strptime(last_date, old_date_format).date()
                        today = datetime.date.today()
                        if self.debug_level > 1:
                            print(someday, 'next', today)

                        delta = today - someday
                        # find months
                        months = str(int(delta.days / 30))
                    else:
                        months = '-'

                    p_str += months

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    first_buy_date = self.demat_txn_get_first_buy_date_by_ticker(ticker)

                    old_date_format = "%d-%b-%Y"
                    # new_date_format = '%Y-%m-%d'
                    if first_buy_date != '-':
                        someday = datetime.datetime.strptime(first_buy_date, old_date_format).date()
                        today = datetime.date.today()
                        if self.debug_level > 1:
                            print(someday, 'next', today)

                        delta = today - someday
                        # find years
                        years = int(delta.days / 365)
                    else:
                        # not happening.
                        years = 1

                    if ticker in self.weight_ticker_units_dict:
                        plan_units = int(self.weight_ticker_units_dict[ticker]) * years
                        current_units = self.demat_summary_get_units_by_ticker(ticker)
                        tbd_units = plan_units - current_units
                        if self.debug_level > 0:
                            print(ticker, "years", years, "plan_oku", plan_units, "current_oku", current_units,
                                  "tbd_oku", tbd_units)
                    else:
                        # missing in weight sheet
                        tbd_units = '-'

                    p_str += str(plan_units)

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    p_str += str(current_units)

                    if delimit == '\t':
                        p_str += '\t'
                    else:
                        p_str += ','

                    p_str += str(tbd_units)

                    p_str += '\n'

                    # print once
                    if iter1 == 2:
                        print('Sample output for 1 company :')
                        print(p_str)

                    fh.write(p_str)
                    iter1 += 1
                else:
                    if self.debug_level > 0:
                        print(self.sc_ratio_values[ticker, "reco_type"])
            except ValueError:
                print('except : ValueError :', ticker)
            except KeyError:
                print('except : KeyError :', ticker)

        print("Tickers with bat missing : ", len(bat_missing_list))
        print(bat_missing_list)

        print("\nIndustry list of tickers in ", out_filename_2)

        fh_2 = open(out_filename_2, "w")

        for industry_name in sorted(self.isin_industry_list):
            if self.phealth_values.get((industry_name, "ticker_list")):
                p_str = industry_name
                p_str += ','
                p_str += str(len(self.phealth_values[industry_name, "ticker_list"]))
                p_str += ','
                for ticker in sorted(self.phealth_values[industry_name, "ticker_list"]):
                    p_str += ticker
                    p_str += ','
                p_str += '\n'

            else:
                p_str = industry_name
                p_str += ','
                p_str += '0'
                p_str += '\n'

            fh_2.write(p_str)

        fh_2.close()

        return