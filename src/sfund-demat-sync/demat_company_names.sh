#!/bin/sh

DATA_DEMAT_FILE=$PROJ_PROFILE_DATA_LOC/demat-data/icicidirect/demat-summary-data.csv
REPORTS_DEMAT_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-names.txt

grep -v -e 'Company Name' -e ETF ${DATA_DEMAT_FILE} | sort | awk -F"," '{print $2}' > ${REPORTS_DEMAT_FILE}
