#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE_AMFI=$CONFIG_DATA_LOC/amfi-data/amfi-data-mcap.csv
IN_FILE_RAW_PLAN=$CONFIG_PROFILE_DATA_LOC/plan-data/plan-data-raw.csv
IN_FILE_PROC_PLAN=$CONFIG_PROFILE_DATA_LOC/plan-data/plan-data-proc.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-ticker-only.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-units.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-all-holdings.csv
OUT_FILE_4=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-plus-holdings.csv
OUT_FILE_5=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-zero-holdings.csv

# phase 1
grep -v -e ',Details'  ${IN_FILE_RAW_PLAN} > ${IN_FILE_PROC_PLAN} 

# phase 2
plan_invoke.py ${DEBUG_LEVEL} ${IN_FILE_AMFI} ${IN_FILE_PROC_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
