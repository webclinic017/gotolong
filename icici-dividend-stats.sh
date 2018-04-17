#!/bin/sh

if test $# -lt 2
then
   echo "usage: $0 <op-txn-history.csv> <plain | csv>"
   exit 1
fi

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
# Open it and remove personal details information (Name and Account number)
#   ** line # 4 'Account Number' 
#   ** line # 12 'Transactions list' 
# Clear contents of Balance Column (Last column)
# Save it as OpTransactionHistory17-04-2018.csv file
# upload OpTransactionHistory17-04-2018.csv to stock-market/fy17-18/

DIV_FILE=$1
CSV_OUT=$2

if [[ $CSV_OUT == "csv" ]] 
then

    echo "Date, Company, Dividend"
    cat $DIV_FILE | grep -v -e NEFT -e CASH -e "Int\.Pd" | grep -e ACH -e CMS -e APBS | grep -v -e BLPGCM | sed -e s'/Limited,\//Limited\//g' | sed -e 's/\"//g' | awk -F',' '{ tdate=$3; tcomp=$6; damount=$8; split(tcomp, comp_name, "/"); company = comp_name[2]; printf("%s,%s,%s\n", tdate, company, int(damount)); }' 

else

    echo "Date Company Dividend "
    cat $DIV_FILE | grep -v -e NEFT -e CASH -e "Int\.Pd" | grep -e ACH -e CMS -e APBS | grep -v -e BLPGCM | sed -e s'/Limited,\//Limited\//g' | sed -e 's/\"//g' | awk -F',' '{ tdate=$3; tcomp=$6; damount=$8; split(tcomp, comp_name, "/"); company = comp_name[2]; printf("%s %s %s\n", tdate, company, int(damount)); }' 

fi
