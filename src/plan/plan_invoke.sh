#!/bin/sh

DEBUG_LEVEL=0

IN_FILE_AMFI=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv
IN_FILE_PLAN=$PROJ_PROFILE_DATA_LOC/plan-data/plan-data.csv
OUT_FILE_1=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-phase-1.csv
OUT_FILE_2=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-phase-2.csv
OUT_FILE_3=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-phase-3.csv
OUT_FILE_4=$PROJ_PROFILE_REPORTS_LOC/plan-reports/plan-reports-phase-4.csv

# phase 1
grep -v -e ',Details'  ${IN_FILE_PLAN} > ${OUT_FILE_1}

# phase 2
plan_invoke.py ${DEBUG_LEVEL} ${IN_FILE_AMFI} ${IN_FILE_PLAN} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4}
