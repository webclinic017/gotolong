#!/bin/sh

CONFIG_PROFILE_DATA_LOC=`python -m gotolong_config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong_config profile_reports`

MODULE=demat-txn-stat

BROKER=icicidirect

IN_FILE_TXN=$CONFIG_PROFILE_DATA_LOC/demat-data/${BROKER}/demat-txn-data.csv

# gather stats
OUT_FILE_YEAR=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${BROKER}/${MODULE}_year.csv
OUT_FILE_QTR=$CONFIG_PROFILE_REPORTS_LOC/${MODULE}-reports/${BROKER}/${MODULE}_qtr.csv

echo "processing"

echo "dumping data for year"
icici_direct_stats.sh ${IN_FILE_TXN} year_company all all year > ${OUT_FILE_YEAR}

echo "dumping data for quarter"
icici_direct_stats.sh ${IN_FILE_TXN} year_company all all quarter > ${OUT_FILE_QTR}

echo "done"
