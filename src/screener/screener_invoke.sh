#!/bin/sh

DEBUG_LEVEL=0

# DEBUG_OPTION=-m pdb

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

#IN_FILE_BSE=$CONFIG_DATA_LOC/isin-data/isin-bse-500.csv
#IN_FILE_NSE=$CONFIG_DATA_LOC/isin-data/isin-nse-500.csv
#IN_FILE_AMFI=$CONFIG_DATA_LOC/amfi-data/amfi-data-mcap.csv

#IN_FILE_SC_NAME_ALIASES=$CONFIG_DATA_LOC/screener-data/screener-name-aliases.csv
IN_FILE_1=$CONFIG_DATA_LOC/screener-data/AC500.csv
# IN_FILE_SC_DATA=$CONFIG_DATA_LOC/screener-data/Core.csv

OUT_FILE_1=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-all.csv
OUT_FILE_2=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-buy.csv
OUT_FILE_3=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-buy-ticker-only.csv
OUT_FILE_4=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-hold-ticker-cause.csv
OUT_FILE_5=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-sale-ticker-cause.csv
OUT_FILE_6=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-reco-ticker-cause.csv
OUT_FILE_7=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-reco-ticker-without-cause-gotolong.csv

python screener_invoke.py -d ${DEBUG_LEVEL} -i  ${IN_FILE_1} -o ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${OUT_FILE_6} ${OUT_FILE_7}