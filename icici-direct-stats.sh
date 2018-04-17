#!/bin/sh

if test $# -lt 3
then
   echo "usage: $0 <file> <year_company> <all | 2017>  <all | tcs>"
   echo "usage: $0 <file> <year_company_verbose> <all | 2017>  <all | tcs>"
   echo "usage: $0 <file> <company_year> <all | tcs>   <all |  2017>"
   exit 1
fi

# Developer : Surinder Kumar
# 
# Steps to use the script :
# 1> Login to ICICIDirect site
# 2> Trade & Invest -> Portfolio & Statements  (https://secure.icicidirect.com/IDirectTrading/Trading/Trade.aspx)
# 3> Portfolio -> Equity
# 4> Equity Portfolio Tracker (top right) -> Advanced options
# 5> Download : All Transaction (csv)
# 6> File : 8501317095_PortFolioEqtSummary.csv
# 7> Upload the file to github (stock-market/all-txn/) and rename it to 20180417_PortFolioEqtSummary.csv (change the date)
# 7> Here is a format of the file
# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,
#
# 3> Run Example
# Usage Examples 
# ./idirect-stats.sh portfolio-eqt-summary.csv company_year TCS all
# ./idirect-stats.sh portfolio-eqt-summary.csv year_company 2017 all
# ./idirect-stats.sh portfolio-eqt-summary.csv year_company all gold

# portfolio-eqt-summary.csv
FILE=$1

# action
ACTION=$2

if  [ "$ACTION" = "company_year" ]
then
  COMPANY=$3
  YEAR=$4
else
  YEAR=$3
  COMPANY=$4
fi

if [ "$COMPANY" = "all" ]
then
   # will match all lines
   SPEC_COMPANY=icicidirect
else
   SPEC_COMPANY=$COMPANY
fi

if [ "$YEAR" = "all" ]
then
   # will match all lines
   SPEC_YEAR=icicidirect
else
   SPEC_YEAR=$YEAR
fi


# echo file $1
# echo action $2

if  [ "$ACTION" = "company_year" ]
then

# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,


cat $FILE | grep -i $SPEC_COMPANY | grep -i $SPEC_YEAR | awk -F',' '{ if (prev_company != $1) { prev_company=$1; prev_year=0; prev_month=0; printf("%s - %s\n",$1, $2);} tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); day=substr(tdate,1,2); if (prev_year != year) { prev_year=year; printf("Year %s\n",year);}  if (prev_month != month) { prev_month=month; printf("\t%s\n",month); } printf("\t\t%3s share@value %5s total %5s %4s\n", int($5), int ($6), int($5*$6), $4);   }' 
fi

if [ "$ACTION" = "year_company" ]
then

OUT_FILE=/tmp/year.out
> $OUT_FILE 

new_num_lines=0
old_num_lines=0
portfolio=0
echo "YEAR, Month, TXN#, Sale, Buy, Net, Portfolio"
for year in 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
do
   for month in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
   do
       # echo year $year
       # echo month $month

       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $month | awk -v portfolio=$portfolio -W dump-variables -F','  ' BEGIN {tbuy = 0; tsale =0; tnet=0; company=""; } {tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=tsale; printf("%s, %s, %3s, %6s, %6s, %6s, %7s\n", year, month, NR, int(tsale), int(tbuy), int(tnet), int(portfolio+tnet)); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $7}'`
       fi
       old_num_lines=$new_num_lines

   done
done
   cat $OUT_FILE
fi

if [ "$ACTION" = "year_company_verbose" ]
then

OUT_FILE=/tmp/year_company.out
> $OUT_FILE 

new_num_lines=0
old_num_lines=0
portfolio=0

echo "YEAR, Month, TXN#, Sale, Buy, Net, Portfolio, Companies"
for year in 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
do
   for month in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
   do
       # echo year $year
       # echo month $month

       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $month | awk  -v portfolio=$portfolio -W dump-variables -F','  ' BEGIN {tbuy = 0; tsale =0; company=""; } {tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=-tsale; printf("%s, %s, %3s, %6s, %6s, %6s, %7s, %s\n", year, month, NR, int(tsale), int(tbuy), int(tnet),  int(portfolio+tnet), company); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $7}'`
       fi
       old_num_lines=$new_num_lines

    
   done
done
   cat $OUT_FILE
fi

# end of the file
################################
