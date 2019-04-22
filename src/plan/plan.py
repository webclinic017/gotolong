#!/usr/bin/python

import sys
import re
import csv
import traceback

import cutil.cutil

from amfi.amfi import * 

class Plan(Amfi):

	def __init__(self):
		super(Plan, self).__init__()
		self.multiplier	= 0 
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

			if row_list[1] == "Multiplier":
				self.multiplier = float(row_list[3])/1000.0
				if self.debug_level > 1 :
					print 'multiplier ', self.multiplier
				return

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
				isin = self.get_amfi_isin_by_name(company_name)
				if self.debug_level > 0:
					print isin, company_name
				self.plan_comp_units[isin] = cutil.cutil.get_number(plan_comp_units_list[iter]) * (self.multiplier)
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
		lines = []
		fh = open(out_filename, "w") 
		sorted_items = sorted(self.plan_comp_units, key=self.plan_comp_units.__getitem__, reverse=True)

		for isin in sorted_items: 
			try:
			        comp_name = self.get_amfi_cname_by_code(isin)
				if self.debug_level >= 2:
					print comp_name
				if isin in self.plan_comp_units:
					units_1k = int(self.plan_comp_units[isin])
				else:
					units_1k = 0
				if units_1k > 0: 
					p_str = self.get_amfi_ticker_by_code(isin) 
					p_str += ' '
					p_str += comp_name
					p_str += '\n'
					lines.append(p_str)
			except ValueError:
				print 'except : ValueError :', comp_name
		lines.sort()
		fh.writelines(lines)
		return

	def print_phase2(self, out_filename, sort_type_rank = None, plus_holdings_only = None, zero_holdings_only = None):
		total_units = 0
		cap_units = {}
		fh = open(out_filename, "w") 
		fh.write('comp_name, ticker, isin, plan_units_1k, rank, captype, mcap\n')
		if sort_type_rank:
			sorted_items = sorted(self.amfi_rank, key=self.amfi_rank.__getitem__)
			if self.debug_level > 2:
				print sorted_items
		else:
			sorted_items = sorted(self.plan_comp_units, key=self.plan_comp_units.__getitem__, reverse=True)

		for isin in sorted_items: 
			try:
				# isin = self.get_amfi_isin_by_name(comp_name)
			        comp_name = self.get_amfi_cname_by_code(isin)
				if self.debug_level >= 2:
					print comp_name
				if isin in self.plan_comp_units:
					units_1k = int(self.plan_comp_units[isin])
				else:
					units_1k = 0
				if self.debug_level >= 2:
					print units_1k 
				mcap = self.get_amfi_mcap_by_code(isin)
				captype = self.get_amfi_captype_by_code(isin)
				if self.debug_level > 0:
					print isin, captype 
				rank = self.get_amfi_rank_by_code(isin)
				ticker = self.get_amfi_ticker_by_code(isin)
				total_units += units_1k
				if captype in cap_units:
					cap_units[captype] += units_1k
				else:
					cap_units[captype] = units_1k
			except ValueError:
				print 'except : ValueError :', comp_name

			if plus_holdings_only:
				if units_1k <= 0 :
					continue

			if zero_holdings_only:
				if units_1k > 0 :
					continue

			if sort_type_rank:
				if  rank > 500 and units_1k <= 0:
					continue

			p_str = comp_name
			p_str += ', '
			p_str += ticker 
			p_str += ', '
			p_str += isin 
			p_str += ', '
			if isin in self.plan_comp_units:
				p_str += str(self.plan_comp_units[isin])
			else:
				p_str += '0'
			p_str += ', '
			p_str += str(rank)
			p_str += ', '
			p_str += captype 
			p_str += ', '
			p_str += str(mcap)
			p_str += '\n'
			fh.write(p_str)
		if self.debug_level > 0 :
			print cap_units 
		# Current portfolio distribution 
		p_str = 'Summary'
		p_str += ', '
		p_str += '-' 
		p_str += ', '
		p_str += '-' 
		p_str += ', '
		p_str += str(total_units)
		p_str += ', '
		try:
			p_str += 'large '  + str(int(round(float((cap_units['Large Cap']*100.0)/total_units)))) +' %'
			p_str += ', '
			p_str += 'mid '  + str(int(round(float((cap_units['Mid Cap']*100.0)/total_units)))) + ' %'
			p_str += ', '
			p_str += 'small '  + str(int(round(float(((cap_units['Small Cap']+cap_units['Micro Cap']+cap_units['Nano Cap']+cap_units['Unknown Cap'])*100.0)/total_units)))) + ' %'
			p_str += '\n'
		except KeyError:
			print 'except KeyError'
			traceback.print_exc()
				
		fh.write(p_str)
		
		# Ideal portfolio distribution 
		p_str = 'Ideal'
		p_str += ', '
		p_str += '-' 
		p_str += ', '
		p_str += '-' 
		p_str += ', '
		p_str += '100'
		p_str += ', '
		p_str += 'large '  + '65-70' +' %'
		p_str += ', '
		p_str += 'mid '  + '20' + ' %'
		p_str += ', '
		p_str += 'small '  + '10-15' + ' %'
		p_str += '\n'
		fh.write(p_str)
		fh.close()

	# print all holdings : plus and zero 
	def print_phase3(self, out_filename):
		self.print_phase2(out_filename, True)

	# print plus holdings only
	def print_phase4(self, out_filename):
		self.print_phase2(out_filename, True, True, False)

	# print zero holdings only
	def print_phase5(self, out_filename):
		self.print_phase2(out_filename, True, False, True)

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

