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
   print "usage: " + program_name + " <out_plain | out_csv> <sort_frequency| sort_frquency_name_only|sort_amount|company_name_only> <summary_yes|sumary_no> <debug_level : 1-4> <dividend-bse.csv> ... "
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
bonus_share={}
company_aliases={}
total_dividend = 0

def load_row(row):
	security_code, security_name, company_name, ex_date, purpose, record_date, bc_state_date, bc_end_date, nd_start_date, nd_end_date, actual_payment_date = row
	company_name = company_name.capitalize()
	company_name = company_name.strip()
	try:
		m = re.search("(Bonus issue)(.*)", purpose)
		if m.group(1) != "Bonus issue":
			if debug_level > 1:
				print 'no bonus match', row 
			return
		else:
			companies.append(company_name)

        	if company_name in bonus_share.keys():
			bonus_share[company_name] =  bonus_share[company_name] +',' + m.group(2)
		else:
			bonus_share[company_name] =  m.group(2) 
	except NameError :
		if debug_level > 1:
			print 'NameError', row
	except AttributeError:
		if debug_level > 1:
			print 'AttributeError', row
	
	
def load_data():
	for in_filename in in_filenames:
		with open(in_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				load_row(row)

load_data()

companies.sort()

if sort_type == "company_name_only": 
	for cname in sorted(set(companies)):
		print cname

# calculate frequency of occurence of each company
comp_freq = Counter(companies)

if debug_level > 1:
	print(comp_freq)

if sort_type == "sort_frequency_name_only" :
	for key, value in sorted(comp_freq.items()):
		print key

if sort_type == "sort_frequency" :
	try:
		for key, value in sorted(comp_freq.items(), key=itemgetter(1)):
			if out_type == "out_csv" :
				print key,',', value, ',', bonus_share[key]
			else:
				print key, value, bonus_share[key]
	except KeyError:
		print 'failed kery', key 

if sort_type == "sort_amount" :
	try:
		for key, value in sorted(bonus_share.items(), key=itemgetter(1)):
			if out_type == "out_csv" :
				print key,',', value, ',', comp_freq[key]
			else:
				print key, value, comp_freq [key]
	except KeyError:
		print 'failed kery', key 
