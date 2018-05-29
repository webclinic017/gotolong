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

sect_pv=0
sect_cv=0
sect_tbd=0

def portfolio_value(d, index):
	total = 0
	for k, v in d.items():
		if isinstance(v, dict):
			total += portfolio_value(v, index)
		else:
			if index == 0:
				value = v.split(":")[0] 
			elif index == 1:
				value = v.split(":")[1] 
			elif index == 2:
				value = v.split(":")[2] 
			total = total + int(value)
	return total


def myprint(d, stack_depth):
	global sect_pv
	global sect_cv
	global sect_tbd
        global sort_type

	global leader_k
        global leader_v
        global leader_planned

	leader_planned = 0
	pv_total = 0
	cv_total = 0
	tbd_total = 0

        company_count = 0;
	for k, v in d.items():
		if isinstance(v, dict):

			if stack_depth == 0:
				sect_pv = 0
				sect_cv = 0
				sect_tbd = 0

			pv_total, cv_total, tbd_total = myprint(v, stack_depth + 1)

			sect_pv += pv_total
			sect_cv += cv_total
			sect_tbd += tbd_total
		
			if stack_depth == 0:
				print('Sector ' + k + ' (' + str(sect_pv) + ' : ' + str(sect_cv) + ' : ' + str(sect_tbd) + ')' )
				print('- - - - - - - - - - - - - - - - - - -')
			else:
				if sort_type == "sect_indu_comp_leader":
					print(leader_k + '(' + leader_v +')' + ' | ')

				print('** Industry ' + k + ' (' + str(pv_total) + ' : ' + str(cv_total) + ' : ' + str(tbd_total) + ')' )

			if stack_depth == 1:
				# industry total 
				pv_total = 0
				cv_total = 0
				tbd_total = 0

			if stack_depth == 2:
				# industry total 
				pv_total = 0
				cv_total = 0
				tbd_total = 0

		else:
			planned_value = v.split(":")[0] 
			current_value = v.split(":")[1] 
			tbd_value = v.split(":")[2] 
			pv_total += int(float(planned_value))
			cv_total += int(float(current_value))
			tbd_total += int(float(tbd_value))

			if (planned_value > leader_planned):
				leader_k = k
				leader_v = v

			process_it = False
			if sort_type == "sector_industry_company_tbd":
				if int(float(tbd_value)) > 0:
					process_it = True
			elif sort_type != "sect_indu_comp_leader":
				process_it = True
			if process_it == True:
				company_count += 1
				sys.stdout.write(k + '(' + v +')' + ' | ')
				if company_count%3 == 0:
					print('')
	print('')		
	return pv_total, cv_total, tbd_total 
			

def load_row(row):
	sector_name, industry_name, company_name, inv_multiplier, plan_units, plan_value, present_value, tbd_value, tbd_units, tbd_pct, last_date = row
	if re.match('Present Value', present_value):
		if debug_level > 1:
			print 'Bypassed header : ', row
		return
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
	if int(present_value) >= 0:
		sect_indu_comp[sector_name][industry_name][company_name] = plan_value + ' : '+ present_value + ' : ' + tbd_value
	
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
	print 'Portfolio Distribution : (Target : Current : TBD )'
	print('- - - - - - - - - - - - - - - - - - -')
	myprint(sect_indu_comp, 0)
	print 'Portfolio ' , '(', portfolio_value(sect_indu_comp, 0), ' : ' , portfolio_value(sect_indu_comp, 1), ' : ', portfolio_value(sect_indu_comp, 2), ')'

if sort_type == "sector_industry_company_tbd": 
	print 'Portfolio Distribution : (Target : Current : TBD )'
	print('- - - - - - - - - - - - - - - - - - -')
	myprint(sect_indu_comp, 0)
	print 'Portfolio ' , '(', portfolio_value(sect_indu_comp, 0), ' : ' , portfolio_value(sect_indu_comp, 1), ' : ', portfolio_value(sect_indu_comp, 2), ')'

if sort_type == "sect_indu_comp_leader": 
	print 'Portfolio Distribution : (Target : Current : TBD )'
	print('- - - - - - - - - - - - - - - - - - -')
	myprint(sect_indu_comp, 0)
	print 'Portfolio ' , '(', portfolio_value(sect_indu_comp, 0), ' : ' , portfolio_value(sect_indu_comp, 1), ' : ', portfolio_value(sect_indu_comp, 2), ')'


if sort_type == "industry_name_only": 
	for iname in sorted(set(industries)):
		print iname

if sort_type == "company_name_only": 
	for cname in companies:
		print cname

