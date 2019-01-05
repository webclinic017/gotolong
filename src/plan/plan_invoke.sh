#!/bin/sh

DEBUG_LEVEL=0

IN_FILE_AMFI=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv
IN_FILE_RAW_PLAN=$PROJ_PROFILE_DATA_LOC/plan-data/plan-data-raw.csv
IN_FILE_PROC_PLAN=$PROJ_PROFILE_DATA_LOC/plan-data/plan-data-proc.csv
OUT_FILE_1=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-name.csv
OUT_FILE_2=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-units.csv
OUT_FILE_3=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-all-holdings.csv
OUT_FILE_4=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-plus-holdings.csv
OUT_FILE_5=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-rank-zero-holdings.csv

# phase 1
grep -v -e ',Details'  ${IN_FILE_RAW_PLAN} > ${IN_FILE_PROC_PLAN} 

# phase 2
plan_invoke.py ${DEBUG_LEVEL} ${IN_FILE_AMFI} ${IN_FILE_PROC_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
