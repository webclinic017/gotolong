#!/bin/sh

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

REPORTS_SFUND_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-names.csv

REPORTS_DEMAT_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-summary-names.csv


REPORTS_SFUND_DEMAT_DIFF_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-demat-dumb-diff.csv

REPORTS_SFUND_DEMAT_JOIN_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/sfund-demat-dumb-join.csv

sdiff -s -W -B ${REPORTS_SFUND_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_SFUND_DEMAT_DIFF_FILE}
paste -d, ${REPORTS_SFUND_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_SFUND_DEMAT_JOIN_FILE}
