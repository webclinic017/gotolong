#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE=$CONFIG_DATA_LOC/mstar-data/
OUT_FILE_1=$CONFIG_REPORTS_LOC/mstar-reports/mstar-reports-phase-1.csv
OUT_FILE_2=$CONFIG_REPORTS_LOC/mstar-reports/mstar-reports-phase-2.csv
OUT_FILE_3=$CONFIG_REPORTS_LOC/mstar-reports/mstar-reports-phase-3.csv

python mstar_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
