#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

MODULE=weight


IN_FILE_PLAN=$CONFIG_PROFILE_DATA_LOC/${MODULE}-data/${MODULE}-data.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-ticker-only.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-sort-units.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-sort-name.csv

# phase 2
# python -m pdb ${MODULE}_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
python ${MODULE}_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
