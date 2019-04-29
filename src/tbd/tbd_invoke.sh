#!/bin/sh

DEBUG_LEVEL=0

PROJ_DATA_LOC=`python -m project data`
PROJ_REPORTS_LOC=`python -m project reports`
PROJ_PROFILE_DATA_LOC=`python -m project profile_data`
PROJ_PROFILE_REPORTS_LOC=`python -m project profile_reports`

ISIN_BSE_FILE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
ISIN_NSE_FILE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv
AMFI_FILE=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv
SCREENER_NAME_ALIASES=$PROJ_DATA_LOC/screener-data/screener-name-aliases.csv
PLAN_FILE=$PROJ_PROFILE_DATA_LOC/plan-data/plan-data-proc.csv
DEMAT_FILE=$PROJ_PROFILE_DATA_LOC/demat-data/icicidirect/demat-data.csv
SCREENER_FILE=$PROJ_DATA_LOC/screener-data/screener-data.csv
OUT_FILE_1=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-1-coverage.csv
OUT_FILE_2=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-2-planned.csv
OUT_FILE_3=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-3-tbd.csv
OUT_FILE_4=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-4-tbd-9m-delay.csv
OUT_FILE_5=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-5-tbd-1y-delay.csv
OUT_FILE_6=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-sale-1.csv

# 9 months
DAYS_DIFF_1=270

# 1 year
DAYS_DIFF_2=365

tbd_invoke.py ${DEBUG_LEVEL} ${ISIN_BSE_FILE} ${ISIN_NSE_FILE} ${AMFI_FILE} ${SCREENER_NAME_ALIASES} ${PLAN_FILE} ${DEMAT_FILE} ${SCREENER_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${OUT_FILE_6} ${DAYS_DIFF_1} ${DAYS_DIFF_2}
