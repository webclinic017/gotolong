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
IN_FILE_1=$CONFIG_DATA_LOC/nse-data/nse-52w-hl.csv
OUT_FILE_1=$CONFIG_REPORTS_LOC/nse-reports/nse-reports-52w-hl.csv
OUT_FILE_2=$CONFIG_REPORTS_LOC/nse-reports/nse-reports-52w-hl.txt

python ftwhl.py -t -l ${LOGGING_LEVEL} -i ${IN_FILE_1}  -o ${OUT_FILE_1} ${OUT_FILE_2}

# csv2html -o test.html test/test.csv
