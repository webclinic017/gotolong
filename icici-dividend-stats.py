#!/usr/bin/python

import sys

program_name = sys.argv[0]

if len(sys.argv) != 4 :
   print "usage: " + program_name + " <op-txn-history.csv> <plain | csv> <sort_date|sort_company|sort_company_cons>"
   sys.exit(1) 

in_filename= sys.argv[1]
out_type= sys.argv[2]
sort_type= sys.argv[3]

file_obj = open (in_filename, "r")

for line in file_obj:
	empty1, sno, value_date, txn_date, cheque, txn_remarks, wdraw_amount, deposit_amount, balance, empty2 = line.split(",")
	print txn_date, txn_remarks, deposit_amount

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

#cat $DIV_FILE | grep -v -e NEFT -e CASH -e "Int\.Pd" | grep -e ACH -e CMS -e APBS | grep -v -e BLPGCM | sed -e s'/Limited,\//Limited\//g' | sed -e 's/\"//g' | awk -F',' '{ tdate=$3; tcomp=$6; damount=$8; split(tcomp, comp_name, "/"); company = comp_name[2]; printf("%s %s %s\n", tdate, company, int(damount)); }' | sort --key=$key | awk ' { printf("%s,", $1);  for (i=2; i<NF; i++) { if (i !=2) { printf(" "); } printf("%s",$i); };  printf(",%s\n",$NF); }'

