#!/usr/bin/python

# Developer : Surinder Kumar 
#
# Login to icici bank account using net banking
# My accounts -> Bank Accounts -> View Detailed Statement
# Transaction Date from ... maximum 1 year period
# 01-04-2017 to 31-03-2018
# Advanced Search : Transaction Type : Credit
# Get Statement
# At bottom :  Download details as XLS file
# Save it as OpTransactionHistory17-04-2018.xls (automatic name)
# Open it and Delete first 12 lines
#   ** This remove personal details information (Name and Account number)
#   ** line # 4 'Account Number' 
#   ** line # 12 'Transactions list' 
# Clear contents of Balance Column (Last column)
# Save it as CSV (Comma delimited) (*.csv) : OpTransactionHistory17-04-2018.csv file
# Upload OpTransactionHistory17-04-2018.csv to stock-market/fy17-18/

# TODO
# Handle INT independent as a member of AMR INT
# Handle company with space and no space

import sys
import re
from collections import Counter
from operator import itemgetter

program_name = sys.argv[0]

if len(sys.argv) != 4 :
   print "usage: " + program_name + " <op-txn-history.csv> <plain | csv> <sort_amount|sort_frequency|sort_company>"
   sys.exit(1) 

in_filename= sys.argv[1]
out_type= sys.argv[2]
sort_type= sys.argv[3]
# Error-1, Warn-2, Log-3
debug_level=1
companies=[]
dividend_amount={}

file_obj = open (in_filename, "r")

for line in file_obj:
	# Replace Limited, with just Limited to avoid split error : ValueError
	line = re.sub(r'Limited,','Limited',line)
	line = re.sub(r'Ltd,','Ltd',line)

	
	try:
	  empty1, sno, value_date, txn_date, cheque, txn_remarks, wdraw_amount, deposit_amount, balance, empty2 = line.split(",")
	except ValueError:
          print 'ValueError ', line

	# avoid cases where txn_remarks itself is double quoted
	txn_remarks = re.sub(r'"','', txn_remarks);

        if txn_remarks == "":
		if line != "":
                	if debug_level > 1:
			   print 'empty ' + line
		continue

	if debug_level > 2:
        	# print 'txn_remarks '+ txn_remarks
		pass	
	
        # match for search at begining
	# NEFT or RTGS or MMT - Mobile money Transfer	
	if re.match('NEFT.*|RTGS.*|MMT.*', txn_remarks):
		if debug_level > 2:
			print 'NEFT/RTGS/MMT skipped' + line
		continue

	# CASH deposit
	if re.match('CASH.*', txn_remarks):
		if debug_level > 2:
			print 'CASH skipped' + line
		continue

 	# Interest paid	- anywhere in string
	if re.search('.*:Int\.Pd:.*', txn_remarks):
		if debug_level > 2:
			print 'Int.Pd skipped' + line
		continue
	
 	# APBS / BLPGCM : Aadhaar Payment Bridge System for LPG Subsidy
	if re.match('APBS/.*', txn_remarks):
		if debug_level > 2:
			print 'APBS skipped' + line
		continue

	if re.match('ACH/.*|CMS/.*', txn_remarks):
		# print txn_date, txn_remarks, deposit_amount
                try:
                	remarks_arr = txn_remarks.split('/')
                        deposit_way = remarks_arr[0] 
                        company_name = remarks_arr[1] 
                        comment_str = remarks_arr[2] 
                        # ignore rest
		except ValueError:
			print 'ValueError ' + txn_remarks

                # remove any numbers like year 2017-2018, hyphen etc
                # remove words like DIV, DIVIDEND
                company_name = re.sub('FINAL DIV|FINAL','', company_name)
                company_name = re.sub('FIN DIV|FINDIV','', company_name)
                company_name = re.sub('INT DIV|INTDIV','', company_name)
                company_name = re.sub('DIV|DIV\.|DIVIDEND','', company_name)
                company_name = re.sub('Limited|LIMITED|LTD','Ltd', company_name)
                company_name = re.sub('\d*','', company_name)
                company_name = re.sub('-','', company_name)
                # convert multiple space to single space
                company_name = re.sub(' +', ' ', company_name)
                # remove leading and trailing space
                company_name = company_name.strip()
                company_name = company_name.capitalize()
                '''
                # remove incomplete word
                if len(company_name) == 20:
                     # remove last word which will be mostly incomplete
                     company_name = company_name.rsplit(' ', 1)[0] 
                '''
		# print company_name, deposit_amount
                companies.append(company_name)
                if company_name in dividend_amount.keys():
			if debug_level > 1:                 
                        	print 'dividend amount :', dividend_amount[company_name]
                        	print 'deposit amount :', deposit_amount 
                	dividend_amount[company_name] = int(dividend_amount[company_name]) + int(float(deposit_amount))
                else:
			dividend_amount[company_name] = int(float(deposit_amount))
                        
               
		continue
	
	if debug_level > 1:
		print 'Unknown skipped' + line
	continue	

# sort companies
companies.sort()

# calculate frequency of occurence of each company
comp_freq = Counter(companies)

if debug_level > 1:
	print(comp_freq)

if sort_type == "sort_company" :
	for key, value in sorted(comp_freq.items()):
		if out_type == "csv" :
			print key,',', value, ',', dividend_amount[key] 
		else:
			print key, value, dividend_amount[key] 
elif sort_type == "sort_frequency" :
	for key, value in sorted(comp_freq.items(), key=itemgetter(1)):
		if out_type == "csv" :
			print key,',', value, ',', dividend_amount[key] 
		else:
			print key, value, dividend_amount[key]
elif sort_type == "sort_amount":
	for key, value in sorted(dividend_amount.items(), key=itemgetter(1)) :
		if out_type == "csv" :
			print key,',', value
		else:
			print key, value

print 'total dividend entries : ',  len(companies)
print 'total companies count : ',  len(comp_freq)
