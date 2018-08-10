#!/bin/sh

DEBUG_LEVEL=1

ISIN_BSE_FILE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
ISIN_NSE_FILE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv
AMFI_FILE=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv
PLAN_FILE=$PROJ_PROFILE_DATA_LOC/plan-data/plan-data.csv
DEMAT_FILE=$PROJ_PROFILE_DATA_LOC/demat-data/demat-data.csv
SCREENER_FILE=$PROJ_DATA_LOC/screener-data/screener-data.csv
OUT_FILE_1=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-1.csv
OUT_FILE_2=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-2.csv
OUT_FILE_3=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-3.csv
OUT_FILE_4=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-4.csv
OUT_FILE_5=$PROJ_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-sale-1.csv
# 6 months
DAYS_DIFF=180

tbd_invoke.py ${DEBUG_LEVEL} ${ISIN_BSE_FILE} ${ISIN_NSE_FILE} ${AMFI_FILE} ${PLAN_FILE} ${DEMAT_FILE} ${SCREENER_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${DAYS_DIFF}
