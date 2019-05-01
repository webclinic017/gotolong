#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE_BSE=$CONFIG_DATA_LOC/isin-data/isin-bse-500.csv
IN_FILE_NSE=$CONFIG_DATA_LOC/isin-data/isin-nse-500.csv
OUT_FILE_1=$CONFIG_REPORTS_LOC/isin-reports/isin-reports-phase-1.csv

isin_invoke.py ${DEBUG_LEVEL} ${IN_FILE_BSE} ${IN_FILE_NSE} ${OUT_FILE_1}
