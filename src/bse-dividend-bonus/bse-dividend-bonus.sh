#!/bin/sh

OUT_TYPE=out_csv
DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 all
do
  for SORT_TYPE in sort_frequency sort_amount
  do
	if [[ "${FY}" == "all" ]] ; then
     	./bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${CONFIG_DATA_LOC}/bse-data/dividend/*/bse-*.csv --bonus_file ${CONFIG_DATA_LOC}/bse-data/bonus/*/bse-*.csv > ${CONFIG_REPORTS_LOC}/dividends-bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	else
     	./bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${CONFIG_DATA_LOC}/bse-data/dividend/${FY}/bse-*.csv --bonus_file ${CONFIG_DATA_LOC}/bse-data/bonus/${FY}/bse-*.csv > ${CONFIG_REPORTS_LOC}/dividends-bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

