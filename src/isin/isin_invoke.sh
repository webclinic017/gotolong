#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

#IN_FILE_BSE=$CONFIG_DATA_LOC/isin-data/isin-bse-500.csv
IN_FILE_NSE=$CONFIG_DATA_LOC/isin-data/isin-nse-500.csv
OUT_FILE_1=$CONFIG_REPORTS_LOC/isin-reports/isin-reports.csv
OUT_FILE_2=$CONFIG_REPORTS_LOC/isin-reports/isin-reports-industry-only.csv

# python isin_invoke.py ${DEBUG_LEVEL} ${IN_FILE_BSE} ${IN_FILE_NSE} ${OUT_FILE_1} ${OUT_FILE_2}
# python isin_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE} --out_files ${OUT_FILE_1}
python isin_invoke.py -t -d ${DEBUG_LEVEL} -i ${IN_FILE_NSE} -o ${OUT_FILE_1}  ${OUT_FILE_2}
