#!/usr/bin/env bash

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

OPT1=plan
OPT2=weight

INPUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/${OPT1}-reports/${OPT1}-reports-ticker-only.csv
INPUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/${OPT2}-reports/${OPT2}-reports-ticker-only.csv

OUTPUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/anomaly-reports/${OPT1}-${OPT2}-reports
OUTPUT_FILE_1=${OUTPUT_DIR}/${OPT1}-only.csv
OUTPUT_FILE_2=${OUTPUT_DIR}/${OPT2}-only.csv

mkdir -p ${OUTPUT_DIR}

# comm command
# by default ouput has 3 columns
# column 1 -> only value unique to file 1
# column 2 -> only values unique to file 2
# column 3 -> values present in both file 1 and file2
#
# -1 -> suppresses column 1 (unique to file1)
# -2 -> suppresses column 2 (unique to file2)
# -3 -> suppresses column 3 (comutil to both file1 and file2)

# display only unique values present in file 1 (column 1)
# suppress column 2 and column 3
LC_ALL='C' comm  -23 ${INPUT_FILE_1} ${INPUT_FILE_2}  > ${OUTPUT_FILE_1}

echo check ${OUTPUT_FILE_1}

# display only unique values present in file 2 (column 2)
# suppress column 1 and column 3
LC_ALL='C' comm  -13 ${INPUT_FILE_1} ${INPUT_FILE_2}  > ${OUTPUT_FILE_2}

echo check ${OUTPUT_FILE_2}
