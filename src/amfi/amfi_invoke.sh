#!/bin/sh

DEBUG_LEVEL=0

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

IN_FILE=$PROJ_DATA_LOC/amfi-data/amfi-*.csv
OUT_FILE_1=$PROJ_REPORTS_LOC/amfi-reports/amfi-reports-phase-1.csv

python amfi_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1}
