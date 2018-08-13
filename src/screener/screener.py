#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import cutil.cutil
import cutil.ratio
from isin.isin import *

# S.No.,Name,CMP,Sales,NP 12M,P/E,OPM,EPS 12M,Dividend Payout,Debt / Eq,Int Coverage,Div Yld,PEG,CMP / BV,Avg Div Payout 3Yrs,IV,EV,Mar Cap,Altman Z Scr,Current ratio,ROE 3Yr,Graham Price,Sales Var 5Yrs,Profit Var 5Yrs,EV / EBIT


class Screener(Isin):
	def __init__(self):
		super(Screener, self).__init__()
		self.sc_sno = [] 
		self.sc_name = {} 
		self.sc_cmp = {}
		self.sc_sales = {}
		self.sc_np = {}
		self.sc_pe = {}
		self.sc_opm = {}
		self.sc_eps = {}
		self.sc_dp = {}
		self.sc_d2e = {}
		self.sc_ic = {}
		self.sc_dy = {}
		self.sc_peg = {}
		self.sc_cmp2bv = {}
		self.sc_dp3 = {}
		self.sc_iv = {}
		self.sc_ev = {}
		self.sc_mcap = {}
		self.sc_altmanz = {}
		self.sc_cr = {}
		self.sc_roe3 = {}
		self.sc_graham = {}
		self.sc_sales_var5 = {}
		self.sc_profit_var5 = {}
		self.sc_ev2ebit = {}
		self.sc_pledge = {}
		self.sc_crank = {}
		self.sc_prank = {}
                self.sc_name_aliases = {}
 		self.debug_level = 0 

	def set_debug_level(self, debug_level):
 		self.debug_level = debug_level

	def load_screener_name_aliases(self, sc_aliases_filename):
		with open(sc_aliases_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				sc_name, isin_name = row
				sc_name = sc_name.strip().capitalize()
				isin_name = isin_name.strip().capitalize()
				if self.debug_level > 1: 
					print 'alias ', sc_name
					print 'real ',isin_name 
				self.sc_name_aliases[sc_name] = isin_name 
		print self.sc_name_aliases

	def resolve_screener_name_alias(self, company_name):
		sc_name = company_name.strip().capitalize()
		if sc_name in self.sc_name_aliases.keys():
			company_name = self.sc_name_aliases[sc_name]
		return company_name

	def load_screener_row(self, row):
		try:
			row_list = row
			if len(row_list) == 0:
				if self.debug_level > 1:
					print 'ignored empty row', row_list
				return

			cmp_rs = row_list[2].strip()
			if cmp_rs == 'CMP' or cmp_rs == 'Rs.' or cmp_rs == '' or cmp_rs == 'CMP Rs.' : 
				if self.debug_level > 1:
					print 'ignored CMP / Rs.', row_list
				return

			# S.No.,Name,CMP,Sales,NP 12M,P/E,OPM,EPS 12M,Dividend Payout,Debt / Eq,Int Coverage,Div Yld,PEG,CMP / BV,Avg Div Payout 3Yrs,IV,EV,Mar Cap,Altman Z Scr,Current ratio,ROE 3Yr,Graham Price,Sales Var 5Yrs,Profit Var 5Yrs,EV / EBIT
			sc_sno = cutil.cutil.get_number(row_list[0])
			sc_name = row_list[1]
			sc_name = self.resolve_screener_name_alias(sc_name)
			sc_name = cutil.cutil.normalize_comp_name(sc_name)
			isin_code = self.get_isin_code_by_name(sc_name)
			if isin_code == '':
				print 'unable to get isin_code : ', sc_name
			else:
				sc_sno = isin_code
				if self.debug_level > 1:
					print 'Found isin_code : ', sc_sno, ' for ', sc_name

			sc_cmp = cutil.cutil.get_number(row_list[2])
			sc_sales = cutil.cutil.get_number(row_list[3])
			sc_np = cutil.cutil.get_number(row_list[4])
			sc_pe = cutil.cutil.get_number(row_list[5])
			sc_opm = cutil.cutil.get_number(row_list[6])
			sc_eps = cutil.cutil.get_number(row_list[7])
			sc_dp = cutil.cutil.get_number(row_list[8])
			sc_d2e = cutil.cutil.get_number(row_list[9])
			sc_ic = cutil.cutil.get_number(row_list[10])
			sc_dy = cutil.cutil.get_number(row_list[11])
			sc_peg  = cutil.cutil.get_number(row_list[12])
			sc_cmp2bv = cutil.cutil.get_number(row_list[13])
			sc_dp3  = cutil.cutil.get_number(row_list[14])
			sc_iv  = cutil.cutil.get_number(row_list[15])
			sc_ev  = cutil.cutil.get_number(row_list[16])
			sc_mcap  = cutil.cutil.get_number(row_list[17])
			sc_altmanz = cutil.cutil.get_number(row_list[18])
			sc_cr = cutil.cutil.get_number(row_list[19])
			sc_roe3 = cutil.cutil.get_number(row_list[20])
			sc_graham = cutil.cutil.get_number(row_list[21])
			sc_sales_var5 = cutil.cutil.get_number(row_list[22])
			sc_profit_var5 = cutil.cutil.get_number(row_list[23])
			sc_ev2ebit = cutil.cutil.get_number(row_list[24])
			sc_pledge = cutil.cutil.get_number(row_list[25])

			self.sc_sno.append(sc_sno)

			self.sc_name[sc_sno] = sc_name
			self.sc_cmp[sc_sno] = sc_cmp
			self.sc_sales[sc_sno] = sc_sales
			self.sc_np[sc_sno] = sc_np 
			self.sc_pe[sc_sno] =  sc_pe
			self.sc_opm[sc_sno] = sc_opm 
			self.sc_eps[sc_sno] =  sc_eps
			self.sc_dp[sc_sno] =  sc_dp
			self.sc_d2e[sc_sno] = sc_d2e 
			self.sc_ic[sc_sno] = sc_ic 
			self.sc_dy[sc_sno] = sc_dy 
			self.sc_peg[sc_sno]  = sc_peg
			self.sc_cmp2bv[sc_sno]  = sc_cmp2bv 
			self.sc_dp3[sc_sno]  = sc_dp3 
			self.sc_iv[sc_sno]  = sc_iv 
			self.sc_ev[sc_sno]  = sc_ev 
			self.sc_mcap[sc_sno]  = sc_mcap 
			self.sc_altmanz[sc_sno] = sc_altmanz
			self.sc_cr[sc_sno] = sc_cr 
			self.sc_roe3[sc_sno] = sc_roe3 
			self.sc_graham[sc_sno] = sc_graham 
			self.sc_sales_var5[sc_sno] = sc_sales_var5
			self.sc_profit_var5[sc_sno] = sc_profit_var5 
			self.sc_ev2ebit[sc_sno] =  sc_ev2ebit
			self.sc_pledge[sc_sno] =  sc_pledge
			
			sc_crank = 0
			
			sc_crank += cutil.ratio.get_cscore_opm(sc_opm)
			sc_crank += cutil.ratio.get_cscore_dp(sc_dp)
			sc_crank += cutil.ratio.get_cscore_d2e(sc_d2e)
			sc_crank += cutil.ratio.get_cscore_ic(sc_ic)
			sc_crank += cutil.ratio.get_cscore_dp(sc_dp3)
			sc_crank += cutil.ratio.get_cscore_current_ratio(sc_cr)
			sc_crank += cutil.ratio.get_cscore_pledge(sc_pledge)
			sc_crank += cutil.ratio.get_cscore_altmanz(sc_altmanz)
			if sc_np > 0:
				sc_crank += 1
			if sc_eps > 0:
				sc_crank += 1
			if sc_roe3 > 8:
				sc_crank += 1 
			
			sc_prank = 0
			sc_prank += cutil.ratio.get_pscore_pe(sc_pe)
			sc_prank += cutil.ratio.get_pscore_peg(sc_peg)
			sc_prank += cutil.ratio.get_pscore_pb(sc_cmp2bv)
			sc_prank += cutil.ratio.get_pscore_dy(sc_dy)
			sc_prank += cutil.ratio.get_pscore_iv(sc_cmp, sc_iv)
			sc_prank += cutil.ratio.get_pscore_graham(sc_cmp, sc_graham)
		
			self.sc_crank[sc_sno] = sc_crank
			self.sc_prank[sc_sno] = sc_prank
			
			if self.debug_level > 1:
				print 'score : ', str(sc_sno) , ', ', sc_name , str(sc_crank) , '\n'
			
		except IndexError:
			print 'except ', row
		except:
			print 'except ', row
			traceback.print_exc()
		
	def load_isin_data_both(self, isin_bse_filename, isin_nse_filename):
		self.load_isin_bse_data(isin_bse_filename)
		self.load_isin_nse_data(isin_nse_filename)

	def load_screener_data(self, sc_filename):
		with open(sc_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_screener_row(row)

	def print_phase1(self, out_filename, sort_score = None):
		fh = open(out_filename, "w") 
		fh.write('sc_isin, sc_name, sc_cmp, sc_sales, sc_np, sc_pe, sc_opm, sc_eps, sc_dp3, sc_d2e, sc_ic, sc_dy, sc_peg, sc_cmp2bv, sc_dp3, sc_iv, sc_ev, sc_mcap, sc_altmanz, sc_cr, sc_roe3, sc_graham, sc_sales_var5, sc_profit_var5, sc_ev2ebit, sc_pledge, sc_crank, sc_prank\n')
		if sort_score:
			sorted_input = sorted(self.sc_crank, key=self.sc_crank.__getitem__, reverse=True)
		else:
			sorted_input = sorted(self.sc_sno)

		for sc_sno in sorted_input:
			p_str = str(sc_sno)
			p_str += ', ' 
			p_str += self.sc_name[sc_sno]
			p_str += ', ' 
			if sc_sno in self.sc_cmp:
				p_str += str(self.sc_cmp[sc_sno])
			else:
				p_str += '-'
			p_str += ', ' 
			p_str += str(self.sc_sales[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_np[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_pe[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_opm[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_eps[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_dp[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_d2e[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_ic[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_dy[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_peg[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_cmp2bv[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_dp3[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_iv[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_ev[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_mcap[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_altmanz[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_cr[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_roe3[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_graham[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_sales_var5[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_profit_var5[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_ev2ebit[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_pledge[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_crank[sc_sno])
			p_str += ', ' 
			p_str += str(self.sc_prank[sc_sno])
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def print_phase2(self, out_filename):
		self.print_phase1(out_filename, True)

	def get_sc_sno_by_name(self, req_name):
		for sc_sno in sorted(self.sc_sno):
			sc_name = self.sc_name[sc_sno]
			# try to find a matching company
			if re.match(sc_name.strip(), req_name.strip()):
				if self.debug_level > 1:
					print 'sc: screener found match : ', req_name, ', sc_sno : ', sc_sno 
				return sc_sno
		return 0

	def get_sc_crank_by_sno(self, sc_sno):
		if sc_sno in self.sc_crank:
			return self.sc_crank[sc_sno]
		return 0
	def get_sc_prank_by_sno(self, sc_sno):
		if sc_sno in self.sc_prank:
			return self.sc_prank[sc_sno]
		return 0
	def get_sc_cmp_by_sno(self, sc_sno):
		if sc_sno in self.sc_cmp:
			return self.sc_cmp[sc_sno]
		return 0
	def get_sc_iv_by_sno(self, sc_sno):
		if sc_sno in self.sc_iv:
			return self.sc_iv[sc_sno]
		return 0
	def get_sc_graham_by_sno(self, sc_sno):
		if sc_sno in self.sc_graham:
			return self.sc_graham[sc_sno]
		return 0
