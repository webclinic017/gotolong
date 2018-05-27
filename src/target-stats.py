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
   print "usage: " + program_name + " <out_plain | out_csv> <sort_industry|sort_amount|sort_name|industry_name_only|company_name_only> <summary_yes|sumary_no> <debug_level : 1-4> <target-hist.csv> ... "
   sys.exit(1) 

out_type= sys.argv[1]
sort_type= sys.argv[2]
summary_type= sys.argv[3]
debug_level= int(sys.argv[4])
in_filenames= sys.argv[5:]
# Error-1, Warn-2, Log-3
companies=[]
industries=[]
sectors=[]
dividend_amount={}
company_aliases={}
total_dividend = 0
sect_indu_comp = {}

def myprint(d, stack_depth):
	for k, v in d.items():
		if isinstance(v, dict):
			# to avoid new line
			if stack_depth == 0:
				print('Sector ' + k)
			else:
				print('  Industry ' + k)
			myprint(v, stack_depth + 1)
		else:
			print("    {0} : {1}".format(k, v))

def load_row(row):
	sector_name, industry_name, company_name, inv_multiplier, plan_units, plan_value, present_value, tbd_value, tbd_value, tbd_pct, last_date = row
	company_name = company_name.capitalize()
	company_name = company_name.strip()
	companies.append(company_name)
	industry_name = industry_name.capitalize()
	industry_name = industry_name.strip()
	industries.append(industry_name)
	sector_name = sector_name.capitalize()
	sector_name = sector_name.strip()
	sectors.append(sector_name)
	if not sect_indu_comp.has_key(sector_name):
		sect_indu_comp[sector_name]= {}
	if not sect_indu_comp[sector_name].has_key(industry_name):
		sect_indu_comp[sector_name][industry_name]={}
	sect_indu_comp[sector_name][industry_name][company_name] = present_value
	
def load_data():
	for in_filename in in_filenames:
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				load_row(row)

load_data()

companies.sort()

if sort_type == "sector_name_only": 
	for sname in sorted(set(sectors)):
		print sname

if sort_type == "sector_industry_company": 
	myprint(sect_indu_comp, 0)

if sort_type == "industry_name_only": 
	for iname in sorted(set(industries)):
		print iname

if sort_type == "company_name_only": 
	for cname in companies:
		print cname

