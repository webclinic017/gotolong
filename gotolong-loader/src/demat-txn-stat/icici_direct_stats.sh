#!/bin/sh

CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`
IN_FILE_TXN=$CONFIG_PROFILE_DATA_LOC/demat-data/icicidirect/demat-txn-data.csv

if test $# -lt 3
then
   echo "usage: $0 default  year_company all all year"
   echo ""
   echo "usage: $0 <file | default>  year_company            <all | 2017>     <all | tcs>    <year | quarter | month>"
   echo "usage: $0 <file | default>  year_company_verbose    <all | 2017>     <all | tcs>"
   echo "usage: $0 <file | default>  company_year            <all | tcs>      <all | 2017>"
   echo "default file : $IN_FILE_TXN"
   exit 1
fi

# AWK_DEBUG="-W dump-variables"

# convert this to python : the script has become heavy and slow : improve the performance

# Developer : Surinder Kumar
# 
# Steps to use the script :
# 1> Login to ICICIDirect site
# 2> Trade & Invest -> Portfolio & Statements  (https://secure.icicidirect.com/IDirectTrading/Trading/Trade.aspx)
# 3> Portfolio -> Equity
# 4.1> Grouping : All (to cover zero and negative holdings)
# 4.2> Equity Portfolio Tracker (top right) -> Advanced options
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

if test -z "$FILE"
then
    FILE=default
fi

if test "$FILE" = "default"
then
    FILE=$IN_FILE_TXN
fi

if test ! -e $FILE
then
    echo "file doesn't exist : $FILE"
    exit 1
fi

# action
ACTION=$2

if test -z "$ACTION"
then
    ACTION="year_company"
fi


if  test "$ACTION" = "company_year"
then
  COMPANY=$3
  YEAR=$4

elif test "$ACTION" = "year_company" -o "$ACTION" = "year_company_verbose"
then
  YEAR=$3
  COMPANY=$4
else
  echo "bad action: $ACTION"
fi

if test -z "$COMPANY"
then
    COMPANY=all
fi
  
if test -z "$YEAR"
then
    YEAR=all
fi

if test "$COMPANY" = "all"
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

YQM=$5

if test -z "$YQM"
then
  YQM="year"
fi

case $YQM in
"year" ) YQM=year ;;
"quarter" ) YQM=quarter ;;
"month" ) YQM=month ;;
esac

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
echo "YEAR, Qtr, Month, TXN#, Sale, Buy, Net, Portfolio"
start_year=2007
current_year=$(date +%Y)
for year in `seq $start_year $current_year` 
do

  if [ "$YQM" = "year" ] ; then
       qtr=all
       month=all

       match=$year
       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk -v qtr=$qtr -v month=$month -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; tnet=0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") { month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=tsale; printf("%s, Q%s, %s, %3s, %6s, %6s, %6s, %7s\n", year, qtr, month, NR, int(tsale), int(tbuy), int(tnet), int(portfolio+tnet)); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines

  fi # year

  if [ "$YQM" = "quarter" ]
  then

   month=all
   for qtr in `seq 1 4` 
   do
       # echo year $year
       # echo month $month

       case "$qtr" in
       4)
             qtr_str="-e Jan -e Feb -e Mar"
             ;; 
       1)
             qtr_str="-e Apr -e May -e Jun"
             ;; 
       2)
             qtr_str="-e Jul -e Aug -e Sep"
             ;; 
       3)
             qtr_str="-e Oct -e Nov -e Dec"
             ;; 
       esac

       match=$qtr_str
       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk -v qtr=$qtr -v month=$month -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; tnet=0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") { month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=tsale; printf("%s, Q%s, %s, %3s, %6s, %6s, %6s, %7s\n", year, qtr, month, NR, int(tsale), int(tbuy), int(tnet), int(portfolio+tnet)); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines

   done # qtr

  fi # qtr

  if [ "$YQM" = "month" ]; then

      for month in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
      do

      case "$month" in
        "Jan" | "Feb" | "Mar") qtr=4;;
        "Apr" | "May" | "Jun") qtr=1;;
        "Jul" | "Aug" | "Sep") qtr=2;;
        "Oct" | "Nov" | "Dec") qtr=3;;
      esac

       match=$month
       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk -v qtr=$qtr -v month=$month -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; tnet=0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") { month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=tsale; printf("%s, Q%s, %s, %3s, %6s, %6s, %6s, %7s\n", year, qtr, month, NR, int(tsale), int(tbuy), int(tnet), int(portfolio+tnet)); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines

      done # month 
   fi # month

done # year 
   cat $OUT_FILE
fi

if [ "$ACTION" = "year_company_verbose" ]
then

OUT_FILE=/tmp/year_company.out
> $OUT_FILE 

new_num_lines=0
old_num_lines=0
portfolio=0

echo "YEAR, Qtr, Month, TXN#, Sale, Buy, Net, Portfolio, Companies"

for year in `seq $start_year $current_year` 
do

  if [ "$YQM" = "year" ]; then
     qtr=all
     month=all

     match=$year
     cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk  -v qtr=$qtr -v month=$month -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") {month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=-tsale; printf("%s, Q%s, %s, %3s, %6s, %6s, %6s, %7s, %s\n", year, qtr, month, NR, int(tsale), int(tbuy), int(tnet),  int(portfolio+tnet), company); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines

  fi # year

  if [ "$YQM" = "quarter" ];  then
    month=all
    for qtr in `seq 1 4` 
    do
       # echo year $year
       # echo month $month

       case "$qtr" in

       4) qtr_str="-e Jan -e Feb -e Mar"
          ;; 
       1) qtr_str="-e Apr -e May -e Jun"
          ;; 
       2) qtr_str="-e Jul -e Aug -e Sep"
          ;; 
       3) qtr_str="-e Oct -e Nov -e Dec"
          ;; 
       esac

       match=$qtr_str
       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk -v qtr=$qtr -v month=$month -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") {month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=-tsale; printf("%s, Q%s, %3s, %6s, %6s, %6s, %7s, %s\n", year, qtr, NR, int(tsale), int(tbuy), int(tnet),  int(portfolio+tnet), company); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines

     done # qtr

   fi # quarter
 
   if [ "$YQM" = "month" ]; then

     for month in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
     do

      case "$month" in
        "Jan" | "Feb" | "Mar") qtr=4;;
        "Apr" | "May" | "Jun") qtr=1;;
        "Jul" | "Aug" | "Sep") qtr=2;;
        "Oct" | "Nov" | "Dec") qtr=3;;
      esac

       match=$month
       cat $FILE | grep $year | grep -i $SPEC_YEAR | grep -i $SPEC_COMPANY | grep $match | awk -v qtr=$qtr -v portfolio=$portfolio $AWK_DEBUG -F','  ' BEGIN {tbuy = 0; tsale =0; company=""; } {tdate=$13; year=substr(tdate,8,4); if (month != "all") { month=substr(tdate,4,3); } buysale=$4; company=company" "$1; if (buysale == "Buy") { tbuy += $5*$6; } else { tsale += $5*$6;} } END { if (tbuy != 0 || tsale != 0) { tnet += tbuy; tnet -=-tsale; printf("%s, Q%s, %s, %3s, %6s, %6s, %6s, %7s, %s\n", year, qtr, month, NR, int(tsale), int(tbuy), int(tnet),  int(portfolio+tnet), company); } }'  >> $OUT_FILE 

       new_num_lines=`wc -l $OUT_FILE | awk '{print $1}'`
       if [[ "$new_num_lines" -ne "$old_num_lines" ]]
       then
         # get portfolio value 
         portfolio=`tail -1 $OUT_FILE | awk '{print $8}'`
       fi
       old_num_lines=$new_num_lines
    
     done # month
   fi # month

done # year
   cat $OUT_FILE
fi

# end of the file
################################
