#!/bin/sh

DEBUG_LEVEL=0

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

IN_FILE=$PROJ_DATA_LOC/mstar-data/
OUT_FILE_1=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-1.csv
OUT_FILE_2=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-2.csv
OUT_FILE_3=$PROJ_REPORTS_LOC/mstar-reports/mstar-reports-phase-3.csv

python mstar_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
