#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import cutil.cutil

class Screener(object):
	def __init__(self):
		super(Screener, self).__init__()
		self.sc_name = [] 
		self.sc_cmp = {}
		self.sc_iv = {}
		self.sc_mos = {}
 		self.debug_level = 0 

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level


	def load_screener_row(self, row):
		try:
			row_list = row
			if len(row_list) == 0:
				if self.debug_level > 1:
					print 'ignored empty row', row_list
				return

			cmp_rs = row_list[2]
			if cmp_rs == 'CMP' or cmp_rs == 'Rs.' or cmp_rs == '': 
				if self.debug_level > 1:
					print 'ignored CMP / Rs.', row_list
				return

			sc_name = row_list[1]
			sc_cmp = row_list[2]
			sc_cmp = int(float(sc_cmp))

			sc_iv = row_list[15]
			if sc_iv == 'NaN':
				sc_iv = 0
			else:
				sc_iv = int(float(sc_iv))

			sc_mos = row_list[24]
			if sc_mos == 'NaN':
				sc_mos = 0
			else:
				sc_mos = int(float(sc_mos))

			sc_name = cutil.cutil.normalize_comp_name(sc_name)

			self.sc_cmp[sc_name] = sc_cmp
			self.sc_iv[sc_name]   = sc_iv
			self.sc_mos[sc_name] = sc_mos
			self.sc_name.append(sc_name)

			if self.debug_level > 1:
				print 'sc_name : ', sc_name , '\n'
				print 'sc_iv : ', sc_iv , '\n'
				print 'sc_mos : ', sc_mos , '\n'

		except IndexError:
			print 'except ', row
		except:
			print 'except ', row
			traceback.print_exc()
		
	def load_screener_data(self, in_filename):
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_screener_row(row)

	def print_phase1(self, out_filename, sort_mos = None):
		fh = open(out_filename, "w") 
		fh.write('sc_name, sc_cmp, sc_iv, sc_mos\n')

		if sort_mos:
			sorted_input = sorted(self.sc_mos, key=self.sc_mos.__getitem__, reverse=True)
		else:
			sorted_input = sorted(self.sc_name)

		for sc_name in sorted_input:
			p_str = sc_name 
			p_str += ', ' 
			if sc_name in self.sc_cmp:
				p_str += str(self.sc_cmp[sc_name])
			else:
				p_str += '-'
			p_str += ', ' 
			if sc_name in self.sc_iv:
				p_str += str(self.sc_iv[sc_name])
			else:
				p_str += '-'
			p_str += ', ' 
			if sc_name in self.sc_mos:
				p_str += str(self.sc_mos[sc_name])
			else:
				p_str += '-'
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def print_phase2(self, out_filename):
		self.print_phase1(out_filename, True)

	def get_sc_mos_by_name(self, req_name):
		req_name = re.sub('\s+', ' ', req_name).strip()
		for sc_name  in sorted(self.sc_name):
			# try to find a matching company
			sc_name = sc_name.strip()
			if re.match(req_name, sc_name):
				if self.debug_level > 1:
					print 'found match : name : ', req_name
				return self.sc_mos[sc_name] 
		if self.debug_level > 1:
			print 'demat not found : req_name :',req_name,':'
		return ''

