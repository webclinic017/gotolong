#!/bin/sh

DEBUG_LEVEL=1

# DEBUG_OPTION=-m pdb

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

IN_FILE_1=$CONFIG_GLOBAL_DATA_LOC/trendlyne-data/trendlyne-data.csv
OUT_DIR=$CONFIG_GLOBAL_REPORTS_LOC/trendlyne-reports/
OUT_FILE_1=$OUT_DIR/trendlyne-reports.csv

mkdir -p $OUT_DIR

python trendlyne.py -d ${DEBUG_LEVEL} -i ${IN_FILE_1} -o ${OUT_FILE_1}