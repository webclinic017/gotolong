#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
from collections import Counter
from operator import itemgetter

class Demat_Prep:

	def __init__(self, debug_level, in_file, out_file1, out_file2, out_file3, out_file4):
		self.company_name = {}
		self.last_txn_type = {}
		self.buy_qty = {}
		self.buy_price	= {}
		self.sale_qty = {}
		self.sale_price	= {}
		self.last_txn_date = {}
		self.phase1_data = {}
		self.filename = in_file 
		self.out_file1 = out_file1 
		self.out_file2 = out_file2
		self.out_file3 = out_file3 
		self.out_file4 = out_file4 
		self.hold_qty = {}
		self.hold_price	= {}
		self.hold_units	= {}
		self.debug_level = debug_level 

	def load_row(self, row):
		try:
			row_list = row
			comp_id   = row_list[0]
			comp_name = row_list[1]
			txn_type = row_list[3]
			txn_qty = row_list[4]
			txn_price = str(int(float(row_list[5])))
			txn_date = row_list[12]


			p_str = comp_id 
			p_str += ','
			p_str += comp_name 
			p_str += ','
			p_str += txn_type
			p_str += ','
			p_str += txn_qty
			p_str += ','
			p_str += txn_price
			p_str += ','
			p_str += txn_date
			p_str += '\n'
	
			if comp_id in self.phase1_data:	
				self.phase1_data[comp_id] += p_str	
			else:
				self.phase1_data[comp_id] = p_str	
				

			self.company_name[comp_id] = comp_name 
			if txn_type == "Buy":
				if comp_id in self.buy_qty:
                        		self.buy_qty[comp_id] += int(txn_qty)
                        		self.buy_price[comp_id]    += int(float(txn_price)) * int(txn_qty)
				else:
                        		self.buy_qty[comp_id] = int(txn_qty) 
                        		self.buy_price[comp_id]    = int(float(txn_price)) * int(txn_qty)
			else:
				if comp_id in self.sale_qty:
                        		self.sale_qty[comp_id] += int(txn_qty)
                        		self.sale_price[comp_id]    += int(float(txn_price)) * int(txn_qty)
				else:
                        		self.sale_qty[comp_id] = int(txn_qty)
                        		self.sale_price[comp_id]    = int(float(txn_price)) * int(txn_qty)
		
			# skip updating bonus entries	
			if txn_price != 0:	
				self.last_txn_type[comp_id]  = txn_type 
                        	self.last_txn_date[comp_id]  = txn_date 

		except:
			print "Unexpected error:", sys.exc_info()

	def load_data(self):
		with open(self.filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_row(row)
		self.prepare_data()
		# sorted(self.phase1_data, key=lambda dct: dct['comp_id'])	
		# sorted(self.phase1_data, key=operator.itemgetter('comp_id'))	

	def prepare_data(self):
		for comp_id in sorted(self.phase1_data):
			if comp_id == 'Stock Symbol':
				continue
			
			if comp_id in self.sale_qty:
				hold_qty = self.buy_qty[comp_id] - self.sale_qty[comp_id]
			else:
				hold_qty = self.buy_qty[comp_id]
			
			# store 
			self.hold_qty[comp_id] = hold_qty
			
			if hold_qty > 0:
				if comp_id in self.sale_price:
					hold_price = self.buy_price[comp_id] - self.sale_price[comp_id]
				else:
					hold_price = self.buy_price[comp_id]
			else:
				hold_price = 0
			
			# store 
			self.hold_price[comp_id] = hold_price
			
			if hold_qty > 0:
				hold_units = hold_price/1000
			else:
				hold_units = 0
			# store 
			self.hold_units[comp_id] = hold_units


	def print_phase1(self):
		fh = open(self.out_file1, "w") 
		fh.write('comp_id, comp_name, action, qty, price, txn_date\n')
		for comp_id in sorted(self.phase1_data):
			fh.write(self.phase1_data[comp_id])
		fh.close()

	def print_phase2(self):
		fh = open(self.out_file2, "w") 
		fh.write('comp_id, comp_name, buy_qty, sale_qty, buy_price, sale_price, last_txn_type, last_txn_date\n')
		for comp_id in sorted(self.phase1_data):
			if comp_id == 'Stock Symbol':
				continue
			p_str = comp_id
			p_str += ','
			p_str += self.company_name[comp_id] 
			p_str += ','
			p_str += str(self.buy_qty[comp_id])
			p_str += ','
			if comp_id in self.sale_qty:
				p_str += str(self.sale_qty[comp_id])
			else:
				p_str += '0' 
			p_str += ','
			p_str += str(self.buy_price[comp_id])
			p_str += ','
			if comp_id in self.sale_price:
				p_str += str(self.sale_price[comp_id])
			else:
				p_str += '0' 
			p_str += ','
			p_str += self.last_txn_type[comp_id] 
			p_str += ','
			p_str += self.last_txn_date[comp_id] 
			p_str += '\n'
			fh.write(p_str)
		fh.close()

	def print_phase3(self, positive_holdings = None):
		if positive_holdings:
			fh = open(self.out_file4,"w") 
		else:
			fh = open(self.out_file3,"w") 
		fh.write('comp_id, comp_name, hold_qty, hold_price, hold_units_1k, last_txn_type, last_txn_date\n')
		for comp_id in sorted(self.phase1_data):
			if comp_id == 'Stock Symbol':
				continue
			p_str = comp_id
			p_str += ','
			p_str += self.company_name[comp_id] 
			p_str += ','
			p_str += str(self.hold_qty[comp_id])
			p_str += ','
			p_str += str(self.hold_price[comp_id])
			p_str += ','
			p_str += str(self.hold_units[comp_id])
			p_str += ','
			p_str += self.last_txn_type[comp_id] 
			p_str += ','
			p_str += self.last_txn_date[comp_id] 
			p_str += '\n'
			if positive_holdings:
				if self.hold_qty[comp_id] > 0:
					fh.write(p_str)
			else:
				fh.write(p_str)
		fh.close()

	def print_phase4(self):
		self.print_phase3(True)

	def get_units(self, comp_id):
		# convert company name to company id	
		return self.hold_units[comp_id]
