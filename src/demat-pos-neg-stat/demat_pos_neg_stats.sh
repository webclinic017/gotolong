#!/bin/sh

# This is to know count of stocks in positive and negative.

CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`
IN_FILE_SUM=$CONFIG_PROFILE_DATA_LOC/demat-pos-neg-stat/icicidirect/demat-summary-data.csv
OUT_FILE_SUM=$CONFIG_PROFILE_REPORTS_LOC/demat-pos-neg-stat-reports/demat-pos-neg-stat-reports.csv

DEBUG=0

if test $DEBUG -eq 1
then
  echo file : $IN_FILE_TXN
fi

# remove first line
# replace () with - (negative)
# sort on second last field - numerically
cat $IN_FILE_SUM | grep -v -e 'Stock Symbol' | sed -e's/(/-/g' -e's/)//g' | sort -t',' -n -k12,12 | awk -F"," -f demat_pos_neg_stats.awk > $OUT_FILE_SUM
