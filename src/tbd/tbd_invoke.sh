#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

ISIN_BSE_FILE=$CONFIG_DATA_LOC/isin-data/isin-bse-500.csv
ISIN_NSE_FILE=$CONFIG_DATA_LOC/isin-data/isin-nse-500.csv
AMFI_FILE=$CONFIG_DATA_LOC/amfi-data/amfi-data-mcap.csv
SCREENER_NAME_ALIASES=$CONFIG_DATA_LOC/screener-data/screener-name-aliases.csv
PLAN_FILE=$CONFIG_PROFILE_DATA_LOC/plan-data/plan-data-proc.csv
DEMAT_FILE=$CONFIG_PROFILE_DATA_LOC/demat-data/icicidirect/demat-data.csv
SCREENER_FILE=$CONFIG_DATA_LOC/screener-data/screener-data-account1.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-1-coverage.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-2-planned-nocond.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-3-planned-cond.csv
OUT_FILE_4=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-4-planned-allyear-cond-mos-25.csv
OUT_FILE_5=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-5-tbd-all-year-cond.csv
OUT_FILE_6=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-6-tbd-1y-nocond.csv
OUT_FILE_7=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-buy-7-tbd-1y-cond.csv
OUT_FILE_8=$CONFIG_PROFILE_REPORTS_LOC/tbd-reports/tbd-reports-phase-sale-1.csv

# 1 year
DAYS_DIFF_1=365

# 9 months
DAYS_DIFF_2=270

# margin of safety 25%
MOS_1=25

# margin of safety 50%
MOS_2=50

tbd_invoke.py ${DEBUG_LEVEL} ${ISIN_BSE_FILE} ${ISIN_NSE_FILE} ${AMFI_FILE} ${SCREENER_NAME_ALIASES} ${PLAN_FILE} ${DEMAT_FILE} ${SCREENER_FILE} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${OUT_FILE_6} ${OUT_FILE_7} ${OUT_FILE_8} ${DAYS_DIFF_1} ${DAYS_DIFF_2} ${MOS_1} ${MOS_2}
