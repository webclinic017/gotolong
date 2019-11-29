# !/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from amfi.amfi import *
from screener.screener import *
from trendlyne.trendlyne import *


class Gfin(Screener, Trendlyne):

    def __init__(self):
        super(Gfin, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.debug_level = 0
        print('init : Gfin')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def gfin_dump_report(self, out_filename):

        delimit = "\t"
        fh = open(out_filename, "w")

        if delimit == "\t":
            p_str = "ticker\tbat\tcmp\tlow_52w\thigh_52w\tmos"
        else:
            p_str = "ticker,high_52w,low_52w,cmp,bat,mos"

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


                    p_str += self.tl_ratio_values[ticker, "bat"]

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
        return