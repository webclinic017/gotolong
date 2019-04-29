#!/bin/sh

DEBUG_LEVEL=0

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

IN_FILE_BSE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
IN_FILE_NSE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv

IN_FILE_AMFI=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv

IN_FILE_SC_NAME_ALIASES=$PROJ_DATA_LOC/screener-data/screener-name-aliases.csv
IN_FILE_SC_DATA=$PROJ_DATA_LOC/screener-data/screener-data.csv

OUT_FILE_1=$PROJ_REPORTS_LOC/screener-reports/screener-reports-phase-1.csv
OUT_FILE_2=$PROJ_REPORTS_LOC/screener-reports/screener-reports-phase-2.csv

screener_invoke.py ${DEBUG_LEVEL} ${IN_FILE_BSE} ${IN_FILE_NSE} ${IN_FILE_AMFI} ${IN_FILE_SC_NAME_ALIASES} ${IN_FILE_SC_DATA} ${OUT_FILE_1} ${OUT_FILE_2}
