#!/bin/sh

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

OUT_TYPE=out_plain
SUMMARY_TYPE=summary_no
DEBUG_LEVEL=0

FY=all

for SORT_TYPE in company_name_only industry_name_only sector_name_only sector_industry_company sector_industry_company_tbd sect_indu_comp_leader comp_tbd
do
	if test ${SORT_TYPE} == "comp_tbd"; then
		OUT_EXT=csv
	else
		OUT_EXT=txt
	fi

	python target-stats.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${CONFIG_GLOBAL_DATA_LOC}/sample-data/target-hist/*/*-targets.csv  > ${CONFIG_GLOBAL_REPORTS_LOC}/targets/${FY}/${FY}-${SORT_TYPE}.${OUT_EXT}

done
