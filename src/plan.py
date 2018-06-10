#!/usr/bin/python

import sys
import re
import csv
import traceback
from collections import Counter
from operator import itemgetter

class Plan:

	def __init__(self, debug_level, filename):
		self.comp_units	= {}
		self.indu_units	= {}
		self.filename = filename
		self.debug_level = debug_level 
		self.last_row = "" 

	def load_row(self, row):
		try:
			row_list = row

			if row_list[1] == "Company":
				# print 'stored last', row
				self.last_row = row
				return

			comp_units_list = row
			comp_units_items_count = len(comp_units_list)

			if comp_units_list[1] != "Units":
				if self.debug_level > 1:
					print 'Bypassed units: ', row
				return

			comp_name_list = self.last_row
			comp_name_items_count = len(comp_name_list)

			if self.debug_level > 1:
				print 'count name : ', comp_name_items_count, "\n"
				print 'count units : ', comp_units_items_count, "\n"
			indu_name = comp_name_list[0]
			# industry units
			indu_units = comp_units_list[2]
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
				company_name = company_name.capitalize()
				company_name = company_name.strip()
				self.comp_units[company_name] = comp_units_list[iter]
			return
		except TypeError:
			print 'except : TypeError : ' , row  , "\n"
		except IndexError:
			print 'except : IndexError : ' , row , "\n"
			traceback.print_exc()

	def load_data(self):
		with open(self.filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_row(row)

	def get_comp_units(self, name):
		if name in self.comp_units:
			return self.comp_units[name]	
		else:
			print 'invalid key :', name

	def print_comp_data(self):
		print self.comp_units

	def size_comp_data(self):
		print len(self.comp_units)

	def get_indu_units(self, name):
		if name in self.indu_units:
			return self.indu_units[name]	
		else:
			print 'invalid key :', name

	def print_indu_data(self):
		print self.indu_units

	def size_indu_data(self):
		print len(self.indu_units)

