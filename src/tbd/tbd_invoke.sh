#!/bin/sh

DEBUG_LEVEL=1

ISIN_BSE_FILE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
ISIN_NSE_FILE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv
PLAN_FILE=$PROJ_DATA_LOC/plan-data/plan-data.csv
DEMAT_FILE=$PROJ_DATA_LOC/demat-data/demat-data.csv
OUT_FILE_1=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-1.csv
OUT_FILE_2=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-2.csv
OUT_FILE_3=$PROJ_DATA_LOC/tbd-data/tbd-data-phase-3.csv

# phase 2
tbd_invoke.py ${DEBUG_LEVEL} ${ISIN_BSE_FILE} ${ISIN_NSE_FILE} ${PLAN_FILE} ${DEMAT_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
