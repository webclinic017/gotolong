#!/bin/sh

DEBUG_LEVEL=0

IN_FILE=$PROJ_DATA_LOC/amfi-data/amfi-*.csv
OUT_FILE_1=$PROJ_REPORTS_LOC/amfi-reports/amfi-reports-phase-1.csv

python amfi_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1}
