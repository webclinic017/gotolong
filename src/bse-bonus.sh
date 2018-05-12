#!/bin/sh

OUT_TYPE=out_csv
DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 all
do
  for SORT_TYPE in sort_frequency sort_amount
  do
	if [[ "${FY}" == "all" ]] ; then
     	./bse-bonus.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/bse-hist/bonus/*/bse-*.csv > ${PROJ_REPORTS_LOC}/bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	else
     	./bse-bonus.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/bse-hist/bonus/${FY}/bse-*.csv > ${PROJ_REPORTS_LOC}/bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

