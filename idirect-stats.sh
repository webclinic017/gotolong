#!/bin/sh

if test $# -lt 3
then
   echo "usage: $0 <file> <company | year> <all | tcs |  2017>"
   exit 1
fi

# Steps to use the script :
# 1> Download ICICIDirect porfolio (all transaction ) and save it in notepad in .csv format (name the file portfolio-eqt-summary.csv)
#
# 2> Here is a format of the file
# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,
#
# 3> Run Example
# Usage Examples 
# ./idirect-stats.sh portfolio-eqt-summary.csv company all
# ./idirect-stats.sh portfolio-eqt-summary.csv company TCS
# ./idirect-stats.sh portfolio-eqt-summary.csv year all
# ./idirect-stats.sh portfolio-eqt-summary.csv year 2008

# portfolio-eqt-summary.csv
FILE=$1

# action
ACTION=$2

# specific action
SPEC=$3

if [ "$SPEC" = "all" ]
then
   # will match all lines
   SPEC=icicidirect
fi

# echo file $1
# echo action $2

if  [ "$ACTION" = "company" ]
then

# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,


cat $FILE | grep -i $SPEC | awk -F',' '{ if (prev_company != $1) { prev_company=$1; prev_year=0; prev_month=0; printf("%s - %s\n",$1, $2);} tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); day=substr(tdate,1,2); if (prev_year != year) { prev_year=year; printf("Year %s\n",year);}  if (prev_month != month) { prev_month=month; printf("\t%s\n",month); } printf("\t\t%s:%s@%s %s\n",$5*$6, $5, $6, $4);   }' 
fi

if [ "$ACTION" = "year" ]
then

for year in 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
do
   for month in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
   do
       # echo year $year
       # echo month $month

       cat $FILE | grep $year | grep $SPEC | grep $month | awk -F','  ' BEGIN {tbuy = 0; tsale =0;} {tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); buysale=$4; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) {printf("%s %s #txn %s sale %s buy %s net %s\n", year, month, NR, tsale, tbuy, tbuy-tsale); } }' 
   done
done
fi

# end of the file
################################

