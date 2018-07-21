#!/bin/sh

DEBUG_LEVEL=0

IN_FILE=$PROJ_DATA_LOC/mstar-data/
OUT_FILE_1=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-1.csv
OUT_FILE_2=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-2.csv
OUT_FILE_3=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-3.csv

python mstar_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
