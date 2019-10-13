#!/bin/sh

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

REPORTS_WEIGHT_FILE=$CONFIG_PROFILE_REPORTS_LOC/weight-demat-reports/weight-names.csv

REPORTS_DEMAT_FILE=$CONFIG_PROFILE_REPORTS_LOC/weight-demat-reports/demat-summary-names.csv

REPORTS_WEIGHT_DEMAT_DIFF_FILE=$CONFIG_PROFILE_REPORTS_LOC/weight-demat-reports/weight-demat-dumb-diff.csv

REPORTS_WEIGHT_DEMAT_JOIN_FILE=$CONFIG_PROFILE_REPORTS_LOC/weight-demat-reports/weight-demat-dumb-join.csv

sdiff -s -W -B ${REPORTS_WEIGHT_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_WEIGHT_DEMAT_DIFF_FILE}
paste -d, ${REPORTS_WEIGHT_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_WEIGHT_DEMAT_JOIN_FILE}
