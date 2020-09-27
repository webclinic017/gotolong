# !/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from datetime import datetime, date

import logging

from amfi.amfi import *
from isin.isin import *
from screener.screener import *
from trendlyne.trendlyne import *
from demat.demat import *

from global_weight.gweight import *

from bhav.bhav import *
from ftwhl.ftwhl import *


class Phealth(Screener, Trendlyne, Demat, Gweight, Bhav, Ftwhl):

    def __init__(self):
        super(Phealth, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.phealth_values = {}
        self.debug_level = 0
        logging.debug('init : phealth')

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def phealth_dump_report(self, out_filename, out_filename_2):

        bat_missing_list = []

        fh = open(out_filename, "w")

        # oku - one k units
        p_str = "ticker,comp_name,bat,cmp,low_52w,high_52w,up_52w_low,mos,txn_gap,plan_oku,cur_oku,tbd_oku,reco_type,reco_cause"
        p_str += '\n'

        fh.write(p_str)

        logging.debug(len(self.sc_nsecode))

        for ticker in self.amfi_ticker_list:

            rank = self.amfi_rank[ticker]
            logging.debug(ticker, 'rank', self.amfi_rank[ticker])

            # capture only large cap and mid cap
            if rank > 250:
                continue

            try:

                p_str = ticker
                p_str += ','

                p_str += self.amfi_cname[ticker]
                p_str += ','

                if self.tl_ratio_values.get((ticker, "bat")):
                    bat = self.tl_ratio_values[ticker, "bat"]
                    p_str += str(bat)
                else:
                    bat = '-'
                    p_str += bat
                    bat_missing_list.append(ticker)
                p_str += ','

                cmp = self.bhav_ticker_cmp_dict[ticker]
                p_str += str(cmp)
                p_str += ','

                low_52w = self.ftwhl_ticker_low_dict[ticker]
                p_str += str(low_52w)
                p_str += ','

                high_52w = self.ftwhl_ticker_high_dict[ticker]
                p_str += str(high_52w)
                p_str += ','

                # up_52w_low
                up_52w_low = round(((cmp - low_52w) * 100.0 / low_52w))
                p_str += str(up_52w_low)
                p_str += ','

                # mos
                if bat != '-':
                    mos = round(((int(bat) - int(cmp)) * 100.0 / int(cmp)))
                else:
                    mos = '-'

                p_str += str(mos)
                p_str += ','

                last_date = self.demat_txn_get_last_date_by_ticker(ticker)

                # old_date_format = "%d-%b-%Y"
                new_date_format = '%Y-%m-%d'
                if last_date != '-':
                    someday = datetime.datetime.strptime(last_date, new_date_format).date()
                    today = datetime.date.today()
                    logging.debug(someday, 'next', today)

                    delta = today - someday
                    # find months
                    months = str(int(delta.days / 30))
                else:
                    months = '-'

                p_str += months
                p_str += ','

                captype = self.amfi_captype[ticker]
                weight = self.gweight_captype_dict[captype]

                plan_units = int(weight)
                current_units = self.demat_sum_get_units_by_ticker(ticker)
                tbd_units = plan_units - current_units

                p_str += str(plan_units)
                p_str += ','

                p_str += str(current_units)
                p_str += ','

                p_str += str(tbd_units)
                p_str += ','

                if (ticker, "reco_type") in self.tl_ratio_values:
                    reco_type = self.tl_ratio_values[ticker, "reco_type"]
                else:
                    reco_type = '-'
                p_str += reco_type
                p_str += ','

                if (ticker, "reco_cause") in self.tl_ratio_values:
                    reco_cause = self.tl_ratio_values[ticker, "reco_cause"]
                else:
                    reco_cause = '-'
                p_str += reco_cause
                p_str += '\n'

                logging.debug(p_str)

                fh.write(p_str)

            except ValueError:
                logging.error('except : ValueError : %s', ticker)
                traceback.print_exc()
            except KeyError:
                logging.error('except : KeyError : %s', ticker)
                traceback.print_exc()

        logging.debug("Tickers with bat missing : ", len(bat_missing_list))
        logging.debug(bat_missing_list)

        return
