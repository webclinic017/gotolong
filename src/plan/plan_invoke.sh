#!/bin/sh

DEBUG_LEVEL=0

IN_FILE=$PROJ_DATA_LOC/plan-data/plan-data.csv
OUT_FILE_1=$PROJ_REPORTS_LOC/plan-reports/plan-reports-phase-1.csv
OUT_FILE_2=$PROJ_REPORTS_LOC/plan-reports/plan-reports-phase-2.csv
OUT_FILE_3=$PROJ_REPORTS_LOC/plan-reports/plan-reports-phase-3.csv

# phase 1
grep -v -e ',Details'  ${IN_FILE} > ${OUT_FILE_1}

# phase 2
plan_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_2} ${OUT_FILE_3}
