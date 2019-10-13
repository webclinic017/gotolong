#!/usr/bin/env bash

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

INPUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-ticker-only.csv

INPUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/weight-reports/weight-reports-ticker-only.csv

OUTPUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/plan-weight-reports/plan-only.csv
OUTPUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/plan-weight-reports/weight-only.csv

# comm command
# by default ouput has 3 columns
# column 1 -> only value unique to file 1
# column 2 -> only values unique to file 2
# column 3 -> values present in both file 1 and file2
#
# -1 -> suppresses column 1 (unique to file1)
# -2 -> suppresses column 2 (unique to file2)
# -3 -> suppresses column 3 (common to both file1 and file2)

# display only unique values present in file 1 (column 1)
# suppress column 2 and column 3
LC_ALL='C' comm  -23 ${INPUT_FILE_1} ${INPUT_FILE_2}  > ${OUTPUT_FILE_1}

echo check ${OUTPUT_FILE_1}

# display only unique values present in file 2 (column 2)
# suppress column 1 and column 3
LC_ALL='C' comm  -13 ${INPUT_FILE_1} ${INPUT_FILE_2}  > ${OUTPUT_FILE_2}

echo check ${OUTPUT_FILE_2}
