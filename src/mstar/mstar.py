#!/usr/bin/python

import sys
import code 
import pandas as pd

# reload(sys)
# sys.setdefaultencoding('utf8')



class Mstar:
	mdf= []
	debug_level = 0

	def set_debug_level(self, debug_level):
		self.debug_level = debug_level

	def get_df(self, stock_type):
		mstar_url = 'https://www.morningstar.in/tools/'
		mstar_url += stock_type  + '.aspx'
	
		print mstar_url
	
		# to skip 0,1,2,3 etc
		dfs = pd.read_html(mstar_url, header =0)

		print len(dfs)

		# sys.exit()

		if self.debug_level > 0:
			for i in range(0, len(dfs)):
				df = dfs[i]
				fname = "mstar_" + stock_type + "_" + str(i) + ".csv"
				df.to_csv(fname, header=None, index=False, encoding='utf-8')

		# last table is interesting
		df = dfs[2]

		# remove line starting with 0,1,2,3,4 etc
		# df.drop(0)

		# print list (df)
		if self.debug_level > 0:
			print list(df.columns.values)

		# [u'Name', u'Rating As on', 'Unnamed: 2', u'Moat', 'Unnamed: 4', u'Valuation', 'Unnamed: 6', u'Uncertainty', 'Unnamed: 8', u'Financial Health', 'Unnamed: 10', u'ISIN', u'Symbol', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17']

		df.columns = ['Name', 'Rating As on', 'U:2', 'MoatRating', 'Moat Value', 'U:5', 'ValuationRating', 'Valuation Value', 'U:8', 'UncertaintyRating', 'Uncertainty Value', 'U:11', 'FinancialHealthRating', 'Financial Health Value', 'U:14', 'ISIN', 'Symbol', 'U:17']

		# drop columns column
		cols = [2,4,5,7,8,10,11,13,14]
		df.drop(df.columns[cols],axis=1,inplace=True)

		return df

	def load_mstar_data(self):
		df = self.mdf
		stock_types = ['undervalued-stocks', 'fairly-valued-stocks', 'wide-moat-stocks', 'narrow-moat-stocks', 'stocks-with-strong-financial-health', 'stocks-with-moderate-financial-health']

		for index in range(0, len(stock_types)):
			df.append(self.get_df(stock_types[index]))

		# concetante row wise
		# df_all = df[0]


		df_all = pd.concat([df[0], df[1], df[2], df[3], df[4], df[5]], ignore_index=True)

		df = df_all

		print list(df.columns.values)

		print 'Before dropping duplicate', len(df)
		df.drop_duplicates(subset=['ISIN'], keep='first', inplace=True)
		print 'After dropping duplicate', len(df)
		
		self.mdf = df

	def filter_data_phase1(self):
		df = self.mdf
		df = df[ df['MoatRating'].isin(['Wide','Narrow']) ]
		print 'MoatRating', len(df)
		df = df[ df['FinancialHealthRating'].isin(['Strong','Moderate','Weak']) ]
		print 'FinancialHealthRating', len(df)
		# exclude Very High, Extreme
		df = df[ df['UncertaintyRating'].isin(['Low','Medium','High']) ]
		print 'UncertaintyRating', len(df)
		df = df[ df['ValuationRating'].isin(['Undervalued', 'Fairly Valued', 'Overvalued']) ]
		print 'ValuationRating', len(df)
		self.mdf = df	

	def print_phase1(self, file):
		df = self.mdf
		fname = file
		df.to_csv(fname, index=False, encoding='utf-8')
		# df.to_csv(fname, header=None, index=False, encoding='utf-8')

	def filter_data_phase2(self):
		df = self.mdf
		df = df[ df['MoatRating'].isin(['Wide','Narrow']) ]
		print 'phase 2 : MoatRating', len(df)
		df = df[ df['FinancialHealthRating'].isin(['Strong','Moderate']) ]
		print 'phase 2 : FinancialHealthRating', len(df)
		# exclude Very High, Extreme
		df = df[ df['UncertaintyRating'].isin(['Low','Medium','High']) ]
		print 'UncertaintyRating', len(df)
		df = df[ df['ValuationRating'].isin(['Undervalued', 'Fairly Valued']) ]
		print 'phase 2 : ValuationRating', len(df)
		self.mdf = df	
	def print_phase2(self, file):
		df = self.mdf
		fname = file
		df.to_csv(fname, index=False, encoding='utf-8')
		# df.to_csv(fname, header=None, index=False, encoding='utf-8')

# column
# print df[:2]

# row format
# print df.ix[2]

# print df
