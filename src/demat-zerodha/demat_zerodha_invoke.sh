#!/bin/sh

DEBUG_LEVEL=1

CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

BROKER=zerodha

IN_FILE_TXN=$CONFIG_PROFILE_DATA_LOC/demat-data/${BROKER}/${BROKER}_demat_data.csv

OUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/demat-reports/${BROKER}
OUT_FILE_1=${OUT_DIR}/demat-reports-ticker-only.csv

mkdir -p ${OUT_DIR}

cat $IN_FILE_TXN  | grep -v -e 'Instrument,' | awk -F',' '{print $1}' > $OUT_FILE_1

echo "check output file : $OUT_FILE_1"
