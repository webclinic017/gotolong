#!/usr/bin/python

import sys
import re
import csv
import traceback

import datetime

from plan.plan import * 
from demat.demat import * 

class Tbd(Plan, Demat):
	def __init__(self):
		super(Tbd, self).__init__()
		# Plan.__init__(debug_level)
		# Demat.__init__(debug_level)
	
	def set_debug_level(self, debug_level):
		self.debug_level = debug_level

	def load_tbd_data(self, plan_filename, demat_filename):
		self.load_demat_data(demat_filename)
		self.load_plan_data(plan_filename)

	def print_tbd_phase1(self, out_filename, tbd_only = None, days_filter = None):
		fh = open(out_filename, "w")
		fh.write('comp_name, plan_units_1k, demat_units_1k, tbd_units, demat_last_txn_date, demat_last_txn_type\n')
		for comp_name in sorted(self.plan_comp_units):
			try:
				plan_units = int(self.plan_comp_units[comp_name])

				if plan_units <= 0:
					print 'no planned units : ', comp_name
					continue	

				demat_comp_id = self.get_demat_comp_id_by_name(comp_name)

				if demat_comp_id == '':
					print 'no demat company found for plan company', comp_name
					continue	

				demat_units = int(self.get_demat_units_by_comp_id(demat_comp_id)) 
				demat_last_txn_date = self.get_demat_last_txn_date_by_comp_id(demat_comp_id)
				if demat_last_txn_date != '':
					last_datetime = datetime.datetime.strptime(demat_last_txn_date, '%d-%b-%Y').date()
					my_delta = datetime.datetime.now().date() - last_datetime
					last_txn_days = my_delta.days
				else:
					my_delta = 0	
				demat_last_txn_type = self.get_demat_last_txn_type_by_comp_id(demat_comp_id)
				tbd_units = plan_units - demat_units
				p_str = comp_name
				p_str += ',' 
				p_str += str(plan_units)
				p_str += ',' 
				p_str += str(demat_units)
				p_str += ',' 
				p_str += str(tbd_units) 
				p_str += ',' 
				p_str += demat_last_txn_date 
				p_str += ',' 
				p_str += demat_last_txn_type
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
				print 'except : ValueError :', comp_name
		fh.close()

	def print_tbd_phase2(self, out_filename):
		self.print_tbd_phase1(out_filename, True)

	def print_tbd_phase3(self, out_filename, days_filter):
		self.print_tbd_phase1(out_filename, True, days_filter)
