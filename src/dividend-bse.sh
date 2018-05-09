#!/bin/sh

dividend-bse.py out_plain sort_frequency summary_yes 1 


DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1718
do
  for SORT_TYPE in sort_frequency 
  do
     	./dividend-bse.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/sample-data/bse-hist/${FY}/bse-*.csv > ${PROJ_REPORTS_LOC}/dividends/${FY}/bse-${FY}-${SORT_TYPE}.csv
  done
done

