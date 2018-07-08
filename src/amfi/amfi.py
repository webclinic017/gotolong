#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import cutil.cutil

class Amfi(object):
	def __init__(self):
		super(Amfi, self).__init__()
		# isin number
		self.amfi_isnu = [] 
		# serial number
		self.amfi_senu = {}
		self.amfi_cname = {}
		self.amfi_ticker = {}
		self.amfi_mcap = {}
		self.amfi_captype = {}
 		self.debug_level = 0 

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level

	def load_amfi_row(self, row):
		try:
			row_list = row
			if len(row_list) == 0:
				print 'ignored empty row', row_list
				return

			serial_number = row_list[0]
			if serial_number == 'Sr. No.':
				print 'skipped header line', row_list
				return

			serial_number = cutil.cutil.get_number(serial_number)

			comp_name = row_list[1]
			isin_number = row_list[2]
			comp_ticker = row_list[3].upper().strip()
			if comp_ticker == '':
				comp_ticker = row_list[5]
			avg_mcap = cutil.cutil.get_number(row_list[9])
			captype = row_list[10]

			comp_name = cutil.cutil.normalize_comp_name(comp_name)

			self.amfi_senu[isin_number] = serial_number
			self.amfi_cname[isin_number] = comp_name 
			self.amfi_ticker[isin_number] = comp_ticker 
			self.amfi_mcap[isin_number] = avg_mcap 
			self.amfi_captype[isin_number] = captype 

			self.amfi_isnu.append(isin_number)

			if self.debug_level > 1:
				print 'comp_name : ', comp_name , '\n'
				print 'isin_number: ', isin_number, '\n'

		except IndexError:
			print 'except ', row
		except:
			print 'except ', row
			traceback.print_exc()
		
	def load_amfi_data(self, in_filename):
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_amfi_row(row)

	def print_phase1(self, out_filename):
		if self.debug_level > 1:
			print self.amfi_name_bse
			print self.amfi_name_nse

		fh = open(out_filename, "w") 
		fh.write('amfi_senu, amfi_cname, amfi_isnu, amfi_ticker, amfi_mcap, amfi_captype\n')
		for amfi_isnu in sorted(self.amfi_senu, key=self.amfi_senu.__getitem__):
			p_str = str(self.amfi_senu[amfi_isnu])
			p_str += ', ' 
			p_str += self.amfi_cname[amfi_isnu]
			p_str += ', ' 
			p_str += amfi_isnu
			p_str += ', ' 
			p_str += self.amfi_ticker[amfi_isnu]
			p_str += ', ' 
			p_str += str(self.amfi_mcap[amfi_isnu])
			p_str += ', ' 
			p_str += self.amfi_captype[amfi_isnu]
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def get_amfi_captype_by_code(self, amfi_isnu):
		if amfi_isnu in self.amfi_name_nse:
			return self.amfi_name_nse[amfi_isnu]
		if amfi_isnu in self.amfi_name_bse:
			return self.amfi_name_bse[amfi_isnu]
		return '-'
