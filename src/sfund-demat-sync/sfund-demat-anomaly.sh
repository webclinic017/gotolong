#!/bin/sh

REPORTS_SFUND_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-sync-reports/sfund-names.txt

REPORTS_DEMAT_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-sync-reports/demat-names.txt

REPORTS_SFUND_DEMAT_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-sync-reports/sfund-demat-diff.txt

sdiff ${REPORTS_SFUND_FILE} ${REPORTS_DEMAT_FILE}  > ${REPORTS_SFUND_DEMAT_FILE}
