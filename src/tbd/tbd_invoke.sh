#!/bin/sh

DEBUG_LEVEL=0

PLAN_FILE=$PROJ_DATA_LOC/plan-data/plan-data.csv
DEMAT_FILE=$PROJ_DATA_LOC/demat-data/demat-data.csv
OUT_FILE_1=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-1.csv
OUT_FILE_2=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-2.csv
OUT_FILE_3=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-3.csv

# phase 2
tbd_invoke.py ${DEBUG_LEVEL} ${PLAN_FILE} ${DEMAT_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
