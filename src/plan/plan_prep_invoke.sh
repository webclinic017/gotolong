#!/bin/sh

DEBUG_LEVEL=0

IN_FILE=$PROJ_DATA_LOC/plan-data/plan-data.csv
OUT_FILE_1=$PROJ_DATA_LOC/plan-data/plan-data-phase-1.csv
OUT_FILE_2=$PROJ_DATA_LOC/plan-data/plan-data-phase-2.csv
OUT_FILE_3=$PROJ_DATA_LOC/plan-data/plan-data-phase-3.csv

# phase 1
grep -v -e ',Details'  ${IN_FILE} > ${OUT_FILE_1}

# phase 2
plan_prep_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_2} ${OUT_FILE_3}
