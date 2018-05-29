#!/bin/sh

OUT_TYPE=out_plain
SUMMARY_TYPE=summary_no
DEBUG_LEVEL=0

FY=all

for SORT_TYPE in company_name_only industry_name_only sector_name_only sector_industry_company sector_industry_company_tbd sect_indu_comp_leader
do
	target-stats.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${PROJ_DATA_LOC}/sample-data/target-hist/*/*-targets.csv  > ${PROJ_REPORTS_LOC}/targets/${FY}/${FY}-${SORT_TYPE}.txt

done
