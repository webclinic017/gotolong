#!/bin/sh

DEBUG_LEVEL=0

# DEBUG_OPTION=-m pdb

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE_1=$CONFIG_DATA_LOC/trendlyne-data/trendlyne-data.csv
OUT_DIR=$CONFIG_REPORTS_LOC/trendlyne-reports/
OUT_FILE_1=$OUT_DIR/trendlyne-reports.csv

mkdir -p $OUT_DIR

python trendlyne_invoke.py -d ${DEBUG_LEVEL} -i ${IN_FILE_1} -o ${OUT_FILE_1}