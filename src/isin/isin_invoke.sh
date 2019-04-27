#!/bin/sh

DEBUG_LEVEL=0

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

IN_FILE_BSE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
IN_FILE_NSE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv
OUT_FILE_1=$PROJ_REPORTS_LOC/isin-reports/isin-reports-phase-1.csv

isin_invoke.py ${DEBUG_LEVEL} ${IN_FILE_BSE} ${IN_FILE_NSE} ${OUT_FILE_1}
