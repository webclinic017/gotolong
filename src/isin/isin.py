#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

class Isin(object):
	def __init__(self):
		super(Isin, self).__init__()
		self.isin_name = {}
 		self.debug_level = 0 

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level

        def normalize_comp_name(self, comp_name):
                comp_name = comp_name.capitalize()
                # remove hyphen (V-guard)
                comp_name = re.sub('-',' ', comp_name)
                # remove . in Dr. lal pathlabs
                comp_name = re.sub('\.','', comp_name)
                # remove ' in Dr Reddy's Laboratories
                comp_name = re.sub('\'','', comp_name)
                comp_name = re.sub('limited','', comp_name)
                comp_name = re.sub('ltd','', comp_name)
                comp_name = re.sub('india','', comp_name)
                # replace and and &
                comp_name = re.sub(' and ',' ', comp_name)
                comp_name = re.sub(' & ',' ', comp_name)
                # remove any characters after (  :
                # TRENT LTD (LAKME LTD)
                comp_name = re.sub('\(.*','', comp_name)
                # convert multiple space to single space
                comp_name = re.sub(' +', ' ', comp_name)
                return comp_name

	def load_isin_row(self, row, bse_nse):
		try:
			row_list = row
			if len(row_list) == 0:
				print 'ignored empty row', row_list
				return

			if bse_nse == "bse":
				comp_name = row_list[1]
				isin_code = row_list[2]
			else:
				comp_name = row_list[0]
				isin_code = row_list[4]

			if isin_code == 'ISIN Code' or isin_code == 'ISIN No.':
				print 'skipped header line', row_list
				return

			comp_name = self.normalize_comp_name(comp_name)
			self.isin_name[isin_code] = comp_name

			if self.debug_level > 1:
				print 'comp_name : ', comp_name , '\n'
				print 'isin_code : ', isin_code , '\n'

		except IndexError:
			print 'except ', row
		except:
			print 'except ', row
			traceback.print_exc()
		
	def load_isin_data(self, in_filename, bse_nse):
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_isin_row(row, bse_nse)

	def load_isin_bse_data(self, in_filename):
		self.load_isin_data(in_filename, 'bse')

	def load_isin_nse_data(self, in_filename):
		self.load_isin_data(in_filename, 'nse')

	def print_phase1(self, out_filename):
		if self.debug_level > 1:
			print self.isin_name

		fh = open(out_filename, "w") 
		fh.write('isin_code, isin_name\n')
		for isin_code in sorted(self.isin_name):
			p_str = str(isin_code)
			p_str += ', ' 
			p_str += self.isin_name[isin_code] 
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def get_isin_code_by_name(self, req_name):
		req_name = re.sub('\s+', ' ', req_name).strip()
		for isin_code in sorted(self.isin_name):
			# try to find a matching company
			comp_name = self.isin_name[isin_code]
			comp_name = comp_name.strip()
			if re.match(req_name, comp_name) or req_name == isin_code:
				if self.debug_level > 1:
					print 'found match : ', req_name
				return isin_code
		if self.debug_level > 1:
			print 'demat not found : req_name :',req_name,':'
		return ''

