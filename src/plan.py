#!/usr/bin/python

import sys
import re
import csv
import traceback
from collections import Counter
from operator import itemgetter

class Plan:

	def __init__(self, debug_level, filenames):
		self.comp_units	= {}
		self.filenames = filenames 
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
		for in_filename in self.filenames:
			with open(in_filename, 'r') as csvfile:
				reader = csv.reader(csvfile)
				for row in reader:
					self.load_row(row)

	def get_units(self, name):
		return self.comp_units[name]	

	def print_data(self):
		print self.comp_units

	def size_data(self):
		print len(self.comp_units)


# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 3 :
   print "usage: " + program_name + " <debug_level : 1-4> <plan.csv> ... "
   sys.exit(1) 

debug_level= int(sys.argv[1])
in_filenames= sys.argv[2:]

plan = Plan(debug_level, in_filenames)

plan.load_data()

plan.print_data()

plan.size_data()
