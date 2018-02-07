#!/bin/sh

# README

# Sample Input
# Ignore first 10 lines
# Each entry template
#Industry,Company,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,TBD %,Last Date,,,,,,,,,
# 
# Input Template (equity-target-units.csv) file
#
# 
#,Investment Multiplier,1000,,Month Name,Jan,Feb,Mar,,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec
#,Number of Companies,210,,Month Number,1,2,3,,4,5,6,7,8,9,10,11,12
#,companies every month (avg),18,Companies,2018,22,30,0,,0,0,0,0,0,0,0,0,0
#,,,Companies,2017,5,2,4,,0,3,41,9,7,26,16,29,17
#,,,Amount,2018,25000,25000,,,,,,,,,,,
#,,,Amount,2017,63680,17471,14897,,8917,38244,150916,59245,71310,95479,,,
#,TOTAL,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,Monthly Investment,Filter Date (Date is before),Months (TBD),,,,,,,,
#,,796,796000,588200,209800,209.80,25000,1-Sep-2017,9.00,,,,,,,,
#,,,,,,,,,,,,,,,,,
#Industry,Company,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,TBD %,Last Date,,,,,,,,,
#Construction & Contracting : Real Estate,HUDCO,2,2000,5600,-3600,-3.60,-1.80,19-Sep-2017,,,,,,,,,
#Chemicals,UPL,2,2000,5000,-3000,-3.00,-1.50,25-Jan-2017,,,,,,,,,



# Sample Output
# CARE (2000) | CRISIL (2000) | ICRA (4000) | 
#Z Misc : Credit Rating (8000) 

#Cox & Kings (2000) | Jubilant Food (3000) | Thomas Cook (2000) | 
#Z Misc : Hospitality (7000) 

#Talvalkar Better Value Fitness (2000) | 
#Z Misc: Fitness (2000) 

#Century Plyboard (2000) | Greenlam (2000) | 
#Z Misc: Woodwork (4000) 

# Portfolio Value 57860


# BASIC CODE

f=equity-target-units.csv
lines=`wc -l $f|awk '{print $1}'`
lines=`expr $lines - 10`
tail -${lines} $f | sort > sort.csv

awk -F "," 'BEGIN {prev_industry=""; ind_total=0; portfolio_total=0;} {if (prev_industry != $1) { printf("\n%s (%d) \n\n", prev_industry, ind_total); portfolio_total+=ind_total; prev_industry=$1; ind_total=$5;} else {ind_total+=$5;} printf("%s (%s) | ", $2, $5); }  END {  printf("\n%s (%d) \n\n", prev_industry, ind_total); printf("Portfolio Value %d\n", portfolio_total); } ' sort.csv
