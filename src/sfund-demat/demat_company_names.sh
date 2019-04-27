#!/bin/sh

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

DATA_DEMAT_FILE=$PROJ_PROFILE_DATA_LOC/demat-data/icicidirect/demat-summary-data.csv
REPORTS_DEMAT_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-names.txt

grep -v -e 'Company Name' -e ETF ${DATA_DEMAT_FILE} | sort | awk -F"," '{print $2}' > ${REPORTS_DEMAT_FILE}
