#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import cutil.cutil

from database.database import *

class Demat(Database):

	def __init__(self):
		super(Demat, self).__init__()
		self.company_name = {}
		self.last_txn_type = {}
		self.buy_qty = {}
		self.buy_price	= {}
		self.sale_qty = {}
		self.sale_price	= {}
		self.last_txn_date = {}
		self.phase1_data = {}
		self.hold_qty = {}
		self.hold_price	= {}
		self.hold_units	= {}
		self.debug_level = 0 
		print 'init : Demat'


	def set_debug_level(self, debug_level):
		self.debug_level = debug_level 


	def load_demat_row(self, row):
		try:
			row_list = row
			# skip header
			if row_list[0] == 'Stock Symbol':
				return
			comp_name = row_list[1]
			isin_code   = (row_list[2]).upper().strip()
			txn_type = row_list[3]
			txn_qty = row_list[4]
			txn_price = str(int(round(float(row_list[5]))))
			txn_date = row_list[12]
			
			p_str = isin_code 
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
			
			if self.debug_level > 1:
				print p_str
			
			if isin_code in self.phase1_data:	
				self.phase1_data[isin_code] += p_str	
			else:
				self.phase1_data[isin_code] = p_str	
				
			self.company_name[isin_code] = cutil.cutil.normalize_comp_name(comp_name)
			if txn_type == "Buy":
				if isin_code in self.buy_qty:
					self.buy_qty[isin_code] += int(txn_qty)
					self.buy_price[isin_code]    += int(round(float(txn_price))) * int(txn_qty)
				else:
					self.buy_qty[isin_code] = int(txn_qty) 
					self.buy_price[isin_code]    = int(round(float(txn_price))) * int(txn_qty)
			else:
				if isin_code in self.sale_qty:
					self.sale_qty[isin_code] += int(txn_qty)
					self.sale_price[isin_code]    += int(round(float(txn_price))) * int(txn_qty)
				else:
					self.sale_qty[isin_code] = int(txn_qty)
					self.sale_price[isin_code]    = int(round(float(txn_price))) * int(txn_qty)
		
			# skip updating bonus entries	
			if txn_price != 0:	
				self.last_txn_type[isin_code]  = txn_type 
				self.last_txn_date[isin_code]  = txn_date 
	
		except:
			print "demat Unexpected error:", sys.exc_info()


	def load_demat_data(self, in_filename):
		table = "demat_txn"
		row_count = self.db_table_count_rows(table)
		if row_count == 0:
			self.insert_demat_data(in_filename)
		else:
			print 'demat_txn data already loaded in db', row_count
		print 'display db data'
		self.load_demat_db()


	def insert_demat_data(self, in_filename):	
		SQL = """insert into demat_txn (stock_symbol, company_name, isin_code, action, quantity, txn_price, brokerage, txn_charges, stamp_duty, segment, stt, remarks, txn_date, exchange, unused1) values (:stock_symbol, :company_name, :isin_code, :action, :quantity, :txn_price, :brokerage, :txn_charges, :stamp_dty, :segment, :stt, :remarks, :txn_date, :exchange, :unused1) """
		cursor = self.db_conn.cursor()
		with open(in_filename, 'rt') as csvfile:
			# future 
			csv_reader = csv.reader(csvfile)
			# insert row
			cursor.executemany(SQL, csv_reader)
			# commit db changes
			self.db_conn.commit()


	def load_demat_db(self):
		table = "demat_txn"
		cursor = self.db_table_load(table)
		for row in cursor.fetchall():
			if self.debug_level > 1 :
				print row
			self.load_demat_row(row)
		self.prepare_demat_data()


	def prepare_demat_data(self):
		for isin_code in sorted(self.phase1_data):
			if isin_code == 'Stock Symbol':
				continue
			
			if isin_code in self.sale_qty:
				hold_qty = self.buy_qty[isin_code] - self.sale_qty[isin_code]
			else:
				hold_qty = self.buy_qty[isin_code]
			
			# store 
			self.hold_qty[isin_code] = hold_qty
			
			if hold_qty > 0:
				if isin_code in self.sale_price:
					hold_price = self.buy_price[isin_code] - self.sale_price[isin_code]
				else:
					hold_price = self.buy_price[isin_code]
			else:
				hold_price = 0
			
			# store 
			self.hold_price[isin_code] = hold_price
			
			if hold_qty > 0:
				hold_units = int(round(float(hold_price)/1000))
			else:
				hold_units = 0
			# store 
			self.hold_units[isin_code] = hold_units
			
			if self.debug_level > 1:
				print 'prepare demat data ', isin_code


	def print_phase1(self, out_filename):
		fh = open(out_filename, "w") 
		fh.write('isin_code, comp_name, action, qty, price, txn_date\n')
		for isin_code in sorted(self.phase1_data):
			if self.debug_level > 1:
				print 'dumping isin', isin_code
			fh.write(self.phase1_data[isin_code])
		fh.close()

	def print_phase2(self, out_filename):
		fh = open(out_filename, "w") 
		fh.write('isin_code, comp_name, buy_qty, sale_qty, buy_price, sale_price, last_txn_type, last_txn_date\n')
		for isin_code in sorted(self.phase1_data):
			if isin_code == 'Stock Symbol':
				continue
			p_str = isin_code
			p_str += ','
			p_str += self.company_name[isin_code] 
			p_str += ','
			p_str += str(self.buy_qty[isin_code])
			p_str += ','
			if isin_code in self.sale_qty:
				p_str += str(self.sale_qty[isin_code])
			else:
				p_str += '0' 
			p_str += ','
			p_str += str(self.buy_price[isin_code])
			p_str += ','
			if isin_code in self.sale_price:
				p_str += str(self.sale_price[isin_code])
			else:
				p_str += '0' 
			p_str += ','
			p_str += self.last_txn_type[isin_code] 
			p_str += ','
			p_str += self.last_txn_date[isin_code] 
			p_str += '\n'
			fh.write(p_str)
		fh.close()

	def print_phase3(self, out_filename, positive_holdings = None):
		fh = open(out_filename,"w") 
		fh.write('isin_code, comp_name, hold_qty, hold_price, hold_units_1k, last_txn_type, last_txn_date\n')
		for isin_code in sorted(self.phase1_data):
			if isin_code == 'Stock Symbol':
				continue
			p_str = isin_code
			p_str += ','
			p_str += self.company_name[isin_code] 
			p_str += ','
			p_str += str(self.hold_qty[isin_code])
			p_str += ','
			p_str += str(self.hold_price[isin_code])
			p_str += ','
			p_str += str(self.hold_units[isin_code])
			p_str += ','
			p_str += self.last_txn_type[isin_code] 
			p_str += ','
			p_str += self.last_txn_date[isin_code] 
			p_str += '\n'
			if positive_holdings:
				if self.hold_qty[isin_code] > 0:
					fh.write(p_str)
			else:
				fh.write(p_str)
		fh.close()

	def print_phase4(self, out_filename):
		self.print_phase3(out_filename, True)

	def get_demat_units_by_isin_code(self, isin_code):
		if isin_code in self.hold_units:
			return self.hold_units[isin_code]
		return 0

	def get_demat_last_txn_date_by_isin_code(self, isin_code):
		if isin_code in self.last_txn_date:
			return self.last_txn_date[isin_code]
		return '' 

	def get_demat_last_txn_type_by_isin_code(self, isin_code):
		if isin_code in self.last_txn_type:
			return self.last_txn_type[isin_code]
		return '' 
