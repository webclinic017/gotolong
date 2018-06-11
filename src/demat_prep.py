#!/usr/bin/python

import sys
import re
import csv
import traceback
from collections import Counter
from operator import itemgetter

class Demat_Prep:

	def __init__(self, debug_level, filename):
		self.company_id = {}
		self.company_name = {}
		self.txn_type = {}
		self.txn_quantity = {}
		self.txn_price	= {}
		self.txn_date = {}
		self.filename = filename
		self.debug_level = debug_level 

	def load_row(self, row):
		try:
			row_list = row
			self.company_id   = row_list[0]
			self.company_name = row_list[1]
			self.txn_type     = row_list[3]
                        self.txn_quantity = row_list[4]
                        self.txn_price    = row_list[5]
                        self.txn_date     = row_list[12]

			p_str = self.company_id
			p_str += ','
			p_str += self.company_name
			p_str += ','
			p_str += self.txn_type
			p_str += ','
			p_str += self.txn_quantity
			p_str += ','
			p_str += self.txn_price
			p_str += ','
			p_str += self.txn_date
		
			print p_str

		except:
			print "Unexpected error:", sys.exc_info()

	def load_data(self):
		with open(self.filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_row(row)

