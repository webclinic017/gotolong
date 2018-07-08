#!/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

class Plan(object):

	def __init__(self):
		super(Plan, self).__init__()
		self.plan_comp_units	= {}
		self.plan_comp_days	= {}
		self.indu_units	= {}
		self.debug_level = 0 
		self.last_row = "" 
		print 'init : Plan'

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level

	def load_plan_row(self, row):
		try:
			row_list = row

			if row_list[1] == "Details":
				if self.debug_level > 1 :
					print 'skipped ', row
				return

			if row_list[1] == "Company":
				# print 'stored last', row
				self.last_row = row
				return

			plan_comp_units_list = row
			plan_comp_units_items_count = len(plan_comp_units_list)

			if plan_comp_units_list[1] != "Units":
				if self.debug_level > 1:
					print 'Bypassed units: ', row
				return

			comp_name_list = self.last_row
			comp_name_items_count = len(comp_name_list)

			if self.debug_level > 1:
				print 'count name : ', comp_name_items_count, "\n"
				print 'count units : ', plan_comp_units_items_count, "\n"
			indu_name = comp_name_list[0]
			# industry units
			indu_units = plan_comp_units_list[2]
			self.indu_units[indu_name] = indu_units 

			if self.debug_level> 1:
				print 'stored industry ', indu_name, ' : ', indu_units
			for iter in range(3, int(comp_name_items_count)): 
				company_name = comp_name_list[iter]
				if company_name == "":
					if self.debug_level > 1:
						print 'found an empty listing', row 
					break
				else:
					if self.debug_level > 2:
						print 'iter ', iter, row, "\n"
				company_name = cutil.cutil.normalize_comp_name(company_name)
				self.plan_comp_units[company_name] = plan_comp_units_list[iter]
			return
		except TypeError:
			print 'except : TypeError : ' , row  , "\n"
		except IndexError:
			print 'except : IndexError : ' , row , "\n"
			traceback.print_exc()

	def load_plan_data(self, in_filename):
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_plan_row(row)

	def print_phase1(self, out_filename):
		# it is covered through shell script
		return

	def print_phase2(self, out_filename, positive_holdings = None):
		fh = open(out_filename, "w") 
		fh.write('comp_name, plan_units_1k\n')
		for comp_name in sorted(self.plan_comp_units, key=self.plan_comp_units.__getitem__, reverse=True):
			try:
				units_1k = int(self.plan_comp_units[comp_name])
			except ValueError:
				print 'except : ValueError :', comp_name
			if positive_holdings and units_1k <= 0 :
				continue
			p_str = comp_name
			p_str += ', ' 
			p_str += self.plan_comp_units[comp_name] 
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def print_phase3(self, out_filename):
		self.print_phase2(out_filename, True)
		
	def get_plan_comp_units(self, name):
		if name in self.plan_comp_units:
			return self.plan_comp_units[name]	
		else:
			print 'invalid key :', name

	def print_comp_data(self):
		print self.plan_comp_units

	def size_comp_data(self):
		print len(self.plan_comp_units)

	def get_indu_units(self, name):
		if name in self.indu_units:
			return self.indu_units[name]	
		else:
			print 'invalid key :', name

	def print_indu_data(self):
		print self.indu_units

	def size_indu_data(self):
		print len(self.indu_units)

