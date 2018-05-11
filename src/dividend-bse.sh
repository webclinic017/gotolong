#!/bin/sh

OUT_TYPE=out_csv
DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 all
do
  for SORT_TYPE in sort_frequency sort_amount
  do
	if [[ "${FY}" == "all" ]] ; then
     	./dividend-bse.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/sample-data/bse-hist/*/bse-*.csv > ${PROJ_REPORTS_LOC}/dividends/${FY}/bse-${FY}-${SORT_TYPE}.csv
	else
     	./dividend-bse.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/sample-data/bse-hist/${FY}/bse-*.csv > ${PROJ_REPORTS_LOC}/dividends/${FY}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

