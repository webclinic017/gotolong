#!/bin/sh

if test -n "${GOTOLONG_LOGGING_LEVEL}"
then
    LOGGING_LEVEL=${GOTOLONG_LOGGING_LEVEL}
else
    LOGGING_LEVEL=INFO
fi

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

# figure this out automatically
IN_FILE_1=$CONFIG_DATA_LOC/nse-data/nse-holiday-list.txt
OUT_FILE_1=$CONFIG_REPORTS_LOC/nse-reports/nse-reports-holiday-list.txt

python nse_holiday.py ${IN_FILE_1} > ${OUT_FILE_1}
