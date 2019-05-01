#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE_1=$CONFIG_PROFILE_DATA_LOC/demat-data/icicidirect/demat-summary-data.csv
IN_FILE_2=$CONFIG_PROFILE_DATA_LOC/demat-data/zerodha/demat-data.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-summary-phase-1.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-summary-names.csv

demat_summary_invoke.py ${DEBUG_LEVEL} ${IN_FILE_1} ${IN_FILE_2} ${OUT_FILE_1} ${OUT_FILE_2}
