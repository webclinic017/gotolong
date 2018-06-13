#!/bin/sh

OUT_TYPE=out_csv
DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 all
do
  for SORT_TYPE in sort_frequency sort_amount
  do
	if [[ "${FY}" == "all" ]] ; then
     	./bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${PROJ_DATA_LOC}/bse-hist/dividend/*/bse-*.csv --bonus_file ${PROJ_DATA_LOC}/bse-hist/bonus/*/bse-*.csv > ${PROJ_REPORTS_LOC}/dividends/${FY}/bse-${FY}-${SORT_TYPE}.csv
	else
     	./bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${PROJ_DATA_LOC}/bse-hist/dividend/${FY}/bse-*.csv --bonus_file ${PROJ_DATA_LOC}/bse-hist/bonus/${FY}/bse-*.csv > ${PROJ_REPORTS_LOC}/dividends/${FY}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

