#!/bin/sh

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

DATA_DEMAT_FILE=$CONFIG_PROFILE_DATA_LOC/demat-data/icicidirect/demat-summary-data.csv
REPORTS_DEMAT_FILE=$CONFIG_PROFILE_REPORTS_LOC/sfund-demat-reports/demat-names.txt

grep -v -e 'Company Name' -e ETF ${DATA_DEMAT_FILE} | sort | awk -F"," '{print $2}' > ${REPORTS_DEMAT_FILE}
