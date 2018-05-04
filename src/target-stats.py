#!/usr/bin/python

# Input Template (equity-target-units.csv) file
# Ignore first 10 lines
# Each entry template
#Industry,Sub Industry, Company,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,TBD %,Last Date,


import sys
import re
import csv
from collections import Counter
from operator import itemgetter

program_name = sys.argv[0]

if len(sys.argv) < 6 :
   print "usage: " + program_name + " <out_plain | out_csv> <sort_industry|sort_amount|sort_name> <summary_yes|sumary_no> <debug_level : 1-4> <target-hist.csv> ... "
   sys.exit(1) 

out_type= sys.argv[1]
sort_type= sys.argv[2]
summary_type= sys.argv[3]
debug_level= int(sys.argv[4])
in_filename= sys.argv[5]
# Error-1, Warn-2, Log-3
companies=[]
dividend_amount={}
company_aliases={}
total_dividend = 0

def load_row(row):
	sector, industry, company_name, inv_multiplier, plan_units, plan_value, present_value, tbd_value, tbd_value, tbd_pct, last_date = row
	company_name = company_name.capitalize()
	company_name = company_name.strip()
	companies.append(company_name)
	
def load_data():
	with open(in_filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			load_row(row)

load_data()

companies.sort()

for cname in companies:
	print cname
