#!/usr/bin/python

import sys
import re
import csv
import traceback

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

	def print_tbd_phase1(self, out_filename, tbd = None):
		fh = open(out_filename, "w")
		fh.write('comp_name, plan_units_1k, demat_units_1k, tbd_units\n')
		for comp_name in sorted(self.plan_comp_units):
			try:
				plan_units = int(self.plan_comp_units[comp_name])
				demat_units = int(self.get_demat_units_by_name(comp_name)) 
				tbd_units = plan_units - demat_units
				p_str = comp_name
				p_str += ',' 
				p_str += str(plan_units)
				p_str += ',' 
				p_str += str(demat_units)
				p_str += ',' 
				p_str += str(tbd_units) 
				p_str += '\n' 
				if tbd:
					if tbd_units > 0:
						fh.write(p_str)
				else:
					fh.write(p_str)
			except ValueError:
				print 'except : ValueError :', comp_name
		fh.close()

	def print_tbd_phase2(self, out_filename):
		self.print_tbd_phase1(out_filename, True)

