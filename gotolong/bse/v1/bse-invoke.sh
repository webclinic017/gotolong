#!/bin/sh

DEBUG_LEVEL=0
CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`


OUT_TYPE=out_csv
SUMMARY_TYPE=summary_yes

for FY in fy1516 fy1617 fy1718 fy1819 fy1920 all
do
  for SORT_TYPE in buyback_count bonus_count dividend_count split_count total_count
  do
        OUT_DIR=${CONFIG_GLOBAL_REPORTS_LOC}/bse-reports/${FY}/
	mkdir -p  ${OUT_DIR}

	if [[ "${FY}" == "all" ]] ; then
     	python bse-invoke.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes \
     	--debug_level ${DEBUG_LEVEL} \
     	--dividend_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/*/bse-*dividend*.csv \
     	--bonus_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/*/bse-*bonus*.csv \
     	--buyback_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/*/bse-*buyback*.csv \
     	--split_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/*/bse-*split*.csv \
     	> ${OUT_DIR}/bse-${FY}-${SORT_TYPE}.csv
	else
     	python bse-invoke.py --out_type out_csv --sort_type ${SORT_TYPE} --summary_type yes \
     	--debug_level ${DEBUG_LEVEL} \
     	--dividend_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/${FY}/bse-*dividend*.csv \
     	--bonus_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/${FY}/bse-*bonus*.csv \
     	--buyback_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/${FY}/bse-*buyback*.csv \
     	--split_file ${CONFIG_GLOBAL_DATA_LOC}/bse-data/${FY}/bse-*split*.csv \
     	> ${OUT_DIR}/bse-${FY}-${SORT_TYPE}.csv
	fi
  done
done

