#!/bin/sh

DEBUG_LEVEL=1

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

MODULE=weight


IN_FILE_PLAN=$CONFIG_PROFILE_DATA_LOC/${MODULE}-data/${MODULE}-data.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-ticker-only.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-sort-units.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${MODULE}-reports-sort-name.csv

# phase 2
# python -m pdb ${MODULE}_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
# TODO : add truncate support 
python ${MODULE}_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
