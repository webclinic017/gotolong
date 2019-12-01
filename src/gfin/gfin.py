# !/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from amfi.amfi import *
from isin.isin import *
from screener.screener import *
from trendlyne.trendlyne import *


class Gfin(Screener, Trendlyne):

    def __init__(self):
        super(Gfin, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.gfin_values = {}
        self.debug_level = 0
        print('init : Gfin')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def gfin_dump_report(self, out_filename, out_filename_2):

        bat_missing_list = []

        delimit = "\t"
        fh = open(out_filename, "w")

        if delimit == "\t":
            p_str = "ticker\tindustry\tbat\tcmp\tlow_52w\thigh_52w\tmos"
        else:
            p_str = "ticker,industry,bat,cmp,low_52w,high_52w,mos"

        p_str += '\n'
        gfin_list = ["price", "low52", "high52"]

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
                        if self.gfin_values.get((industry_name, "ticker_list")):
                            self.gfin_values[industry_name, "ticker_list"].append(ticker)
                        else:
                            self.gfin_values[industry_name, "ticker_list"] = [ticker]
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

                    for gfin_name in gfin_list:
                        # p_str += "'"
                        p_str += '=ROUND(GOOGLEFINANCE(CONCATENATE("NSE:",A'
                        p_str += str(iter1)
                        p_str += '),"'
                        p_str += gfin_name
                        p_str += '"))'
                        # p_str += "'"
                        if delimit == '\t':
                            p_str += '\t'
                        else:
                            p_str += ','

                    p_str += '=ROUND((B'
                    p_str += str(iter1)
                    p_str += '-C'
                    p_str += str(iter1)
                    p_str += ')*100/C'
                    p_str += str(iter1)
                    p_str += ')'

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
            if self.gfin_values.get((industry_name, "ticker_list")):
                p_str = industry_name
                p_str += ','
                p_str += str(len(self.gfin_values[industry_name, "ticker_list"]))
                p_str += ','
                for ticker in sorted(self.gfin_values[industry_name, "ticker_list"]):
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