#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
from collections import Counter
from operator import itemgetter

class Demat_Prep:

	def __init__(self, debug_level, in_file, out_file1, out_file2, out_file3):
		self.company_name = {}
		self.last_txn_type = {}
		self.buy_quantity = {}
		self.buy_price	= {}
		self.sale_quantity = {}
		self.sale_price	= {}
		self.last_txn_date = {}
		self.phase1_data = {}
		self.filename = in_file 
		self.out_file1 = out_file1 
		self.out_file2 = out_file2
		self.out_file3 = out_file3 
		self.debug_level = debug_level 

	def load_row(self, row):
		try:
			row_list = row
			comp_id   = row_list[0]
			comp_name = row_list[1]
			txn_type = row_list[3]
			txn_quantity = row_list[4]
			txn_price = str(int(float(row_list[5])))
			txn_date = row_list[12]


			p_str = comp_id 
			p_str += ','
			p_str += comp_name 
			p_str += ','
			p_str += txn_type
			p_str += ','
			p_str += txn_quantity
			p_str += ','
			p_str += txn_price
			p_str += ','
			p_str += txn_date
			p_str += '\n'
		
			self.phase1_data[comp_id] = p_str	

			self.company_name[comp_id] = comp_name 
			if txn_type == "Buy":
				if comp_id in self.buy_quantity:
                        		self.buy_quantity[comp_id] += txn_quantity 
                        		self.buy_price[comp_id]    += int(float(txn_price)) * int(txn_quantity)
				else:
                        		self.buy_quantity[comp_id] = txn_quantity 
                        		self.buy_price[comp_id]    = int(float(txn_price)) * int(txn_quantity)
			else:
				if comp_id in self.sale_quantity:
                        		self.sale_quantity[comp_id] += txn_quantity
                        		self.sale_price[comp_id]    += int(float(txn_price)) * int(txn_quantity)
				else:
                        		self.sale_quantity[comp_id] = txn_quantity
                        		self.sale_price[comp_id]    = int(float(txn_price)) * int(txn_quantity)
		
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
		# sorted(self.phase1_data, key=lambda dct: dct['comp_id'])	
		# sorted(self.phase1_data, key=operator.itemgetter('comp_id'))	

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
			p_str += self.buy_quantity[comp_id] 
			p_str += ','
			if comp_id in self.sale_quantity:
				p_str += self.sale_quantity[comp_id] 
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

	def print_phase3(self):
		fh = open(self.out_file3,"w") 
		fh.write('comp_id, comp_name, hold_qty, hold_price, hold_units, last_txn_type, last_txn_date\n')
		for comp_id in sorted(self.phase1_data):
			if comp_id == 'Stock Symbol':
				continue
			p_str = comp_id
			p_str += ','
			p_str += self.company_name[comp_id] 
			p_str += ','
			if comp_id in self.sale_quantity:
				p_str += str(int(self.buy_quantity[comp_id]) - int(self.sale_quantity[comp_id]))
			else:
				p_str += self.buy_quantity[comp_id]
			p_str += ','
			if comp_id in self.sale_price:
				p_str += str(self.buy_price[comp_id] - self.sale_price[comp_id])
			else:
				p_str += str(self.buy_price[comp_id])
			p_str += ','
			if comp_id in self.sale_price:
				p_str += str((self.buy_price[comp_id] - self.sale_price[comp_id])/1000)
			else:
				p_str += str((self.buy_price[comp_id])/1000)
			p_str += ','
			p_str += self.last_txn_type[comp_id] 
			p_str += ','
			p_str += self.last_txn_date[comp_id] 
			p_str += '\n'
			fh.write(p_str)
		fh.close()
