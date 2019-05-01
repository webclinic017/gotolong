#!/bin/sh

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

REPORTS_SFUND_FILE=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-names.csv

REPORTS_DEMAT_FILE=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-summary-names.csv


REPORTS_SFUND_DEMAT_DIFF_FILE=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-demat-dumb-diff.csv

REPORTS_SFUND_DEMAT_JOIN_FILE=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-demat-dumb-join.csv

sdiff -s -W -B ${REPORTS_SFUND_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_SFUND_DEMAT_DIFF_FILE}
paste -d, ${REPORTS_SFUND_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_SFUND_DEMAT_JOIN_FILE}
