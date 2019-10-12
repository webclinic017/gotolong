#!/bin/sh

DEBUG_LEVEL=1

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

# figure this out automatically
IN_FILE=$CONFIG_DATA_LOC/amfi-data/out-csv/2019/amfi-mcap-jan-jun-2019.csv
OUT_FILE_1=$CONFIG_REPORTS_LOC/amfi-reports/amfi-reports-phase-1.csv

python amfi_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1}
