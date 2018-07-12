#!/usr/bin/python

import sys
import re
import csv
import traceback

import datetime

from plan.plan import * 
from demat.demat import * 
from isin.isin import * 
from screener.screener import * 

class Tbd(Plan, Demat, Screener):
	def __init__(self):
		super(Tbd, self).__init__()
		# Plan.__init__(debug_level)
		# Demat.__init__(debug_level)
		self.tbd_last_txn_days = {}
		self.tbd_demat_units = {}
		self.tbd_units = {}
		self.tbd_pct = {}
		self.tbd_isin_name = {}
		self.tbd_isin_code = {}
		self.tbd_t500 = {}
		self.tbd_demat_last_txn_date = {}
		self.tbd_demat_last_txn_type = {}

	
	def set_debug_level(self, debug_level):
		self.debug_level = debug_level

	def load_tbd_data(self, isin_bse_filename, isin_nse_filename, plan_filename, demat_filename, screener_filename):
		self.load_isin_bse_data(isin_bse_filename)
		self.load_isin_nse_data(isin_nse_filename)
		self.load_demat_data(demat_filename)
		self.load_plan_data(plan_filename)
		self.load_screener_data(screener_filename)
		self.process_tbd_data()
	
	def process_tbd_data(self):
		for comp_name in sorted(self.plan_comp_units):
			try:
				plan_units = int(self.plan_comp_units[comp_name])
				isin_code = self.get_isin_code_by_name(comp_name)
				self.tbd_isin_code[comp_name] = isin_code	
				if isin_code == '':
					self.tbd_t500[comp_name] =   '-'
					if self.debug_level > 0:
						print 'not in nse 500 ', comp_name
				else:
					self.tbd_t500[comp_name] =   'yes'
				
				demat_units = int(self.get_demat_units_by_isin_code(isin_code)) 
				self.tbd_demat_units[comp_name] = demat_units 
				demat_last_txn_date = self.get_demat_last_txn_date_by_isin_code(isin_code)
				self.tbd_demat_last_txn_date[comp_name] = demat_last_txn_date 
				if demat_last_txn_date != '':
					last_datetime = datetime.datetime.strptime(demat_last_txn_date, '%d-%b-%Y').date()
					my_delta = datetime.datetime.now().date() - last_datetime
					last_txn_days = my_delta.days
				else:
					last_txn_days = 0
				
				self.tbd_last_txn_days[comp_name] = last_txn_days
				
				self.tbd_demat_last_txn_type[comp_name] = self.get_demat_last_txn_type_by_isin_code(isin_code)
				tbd_units = plan_units - demat_units
				if plan_units <= 0:
					tbd_pct = 0
				else:
					tbd_pct = float((100.0*tbd_units)/plan_units)
				tbd_pct = format(tbd_pct, '.2f')
				self.tbd_units[comp_name] = tbd_units
				self.tbd_pct[comp_name] = tbd_pct
			        isin_name = self.get_isin_name_by_code(isin_code)
				if isin_name == '':
					self.tbd_isin_name[comp_name] = comp_name
				else:
					self.tbd_isin_name[comp_name] = isin_name 
			except ValueError:
				print 'except : process: ValueError :', comp_name
	
	def print_tbd_phase1(self, out_filename, plan_only = None, tbd_only = None, days_filter = None):
		fh = open(out_filename, "w")
		fh.write('comp_name, isin, plan_1k, demat_1k, tbd_1k, tbd_pct, last_txn_date, days, type, t500, sc_crank, sc_prank, sc_cmp, sc_iv, sc_graham\n')
		for comp_name in sorted(self.tbd_last_txn_days, key=self.tbd_last_txn_days.__getitem__, reverse=True):
			try:
				plan_units = int(self.plan_comp_units[comp_name])
				if plan_only and plan_units <= 0:
					if self.debug_level > 1:
						print 'no planned units : ', comp_name
					continue	
				
				isin_code = self.tbd_isin_code[comp_name]
				
				if comp_name in self.tbd_demat_units:
					demat_units = int(self.tbd_demat_units[comp_name])
				tbd_units = int(self.tbd_units[comp_name])
				tbd_pct = int(round(float(self.tbd_pct[comp_name])))
				if isin_code == '':
					sc_crank = 0
					sc_prank = 0
					sc_cmp = 0
					sc_iv = 0
					sc_graham = 0
				else:
					sc_crank = self.get_sc_crank_by_sno(isin_code)
					sc_prank = self.get_sc_prank_by_sno(isin_code)
					sc_cmp = self.get_sc_cmp_by_sno(isin_code)
					sc_iv = self.get_sc_iv_by_sno(isin_code)
					sc_graham = self.get_sc_graham_by_sno(isin_code)
				
				last_txn_days = self.tbd_last_txn_days[comp_name]
				p_str = self.tbd_isin_name[comp_name]
				p_str += ','
				p_str += isin_code
				p_str += ',' 
				p_str += str(plan_units)
				p_str += ',' 
				p_str += str(demat_units)
				p_str += ',' 
				p_str += str(tbd_units) 
				p_str += ',' 
				p_str += str(tbd_pct) 
				p_str += ',' 
				p_str += self.tbd_demat_last_txn_date[comp_name]
				p_str += ',' 
				p_str += str(last_txn_days)
				p_str += ',' 
				p_str += self.tbd_demat_last_txn_type[comp_name]
				p_str += ',' 
				p_str += self.tbd_t500[comp_name]
				p_str += ',' 
				p_str += str(sc_crank)
				p_str += ',' 
				p_str += str(sc_prank)
				p_str += ',' 
				p_str += str(sc_cmp)
				p_str += ',' 
				p_str += str(sc_iv)
				p_str += ',' 
				p_str += str(sc_graham)
				p_str += '\n' 
				if tbd_only:
					if tbd_units > 0:
						if days_filter:
							if last_txn_days > days_filter :
								fh.write(p_str)
						else:	
							fh.write(p_str)
				else:
					fh.write(p_str)
			except ValueError:
				print 'except : print : ValueError :', comp_name
				traceback.print_exc()
		fh.close()

	def print_tbd_phase2(self, out_filename):
		self.print_tbd_phase1(out_filename, True)

	def print_tbd_phase3(self, out_filename):
		self.print_tbd_phase1(out_filename, True, True)

	def print_tbd_phase4(self, out_filename, days_filter):
		self.print_tbd_phase1(out_filename, True, True, days_filter)
