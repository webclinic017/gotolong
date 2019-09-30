#!/bin/sh

DEBUG_LEVEL=0
CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


OUT_TYPE=out_csv
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 fy1819 fy1920 all
do
  for SORT_TYPE in sort_frequency sort_amount
  do
	mkdir -p  ${CONFIG_REPORTS_LOC}/dividends-bonus/${FY}/

	if [[ "${FY}" == "all" ]] ; then
     	python bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${CONFIG_DATA_LOC}/bse-data/dividend/*/bse-*.csv --bonus_file ${CONFIG_DATA_LOC}/bse-data/bonus/*/bse-*.csv > ${CONFIG_REPORTS_LOC}/dividends-bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	else
     	python bse-dividend-bonus.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes --debug_level ${DEBUG_LEVEL} --dividend_file ${CONFIG_DATA_LOC}/bse-data/dividend/${FY}/bse-*.csv --bonus_file ${CONFIG_DATA_LOC}/bse-data/bonus/${FY}/bse-*.csv > ${CONFIG_REPORTS_LOC}/dividends-bonus/${FY}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

