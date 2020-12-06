#!/bin/sh

if test -n "${GOTOLONG_LOGGING_LEVEL}"
then
    LOGGING_LEVEL=${GOTOLONG_LOGGING_LEVEL}
else
    LOGGING_LEVEL=INFO
fi

CONFIG_GLOBAL_DATA_LOC=`python -m config global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m config global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

# figure this out automatically
IN_FILE_1=$CONFIG_GLOBAL_REPORTS_LOC/bse-reports/all/bse-all-corpact.csv
OUT_FILE_1=$CONFIG_GLOBAL_REPORTS_LOC/corpact-reports/corpact-reports-phase-1.csv
OUT_FILE_2=$CONFIG_GLOBAL_REPORTS_LOC/corpact-reports/corpact-reports-phase-1.txt

# python amfi_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE} --out_files ${OUT_FILE_1}
python corpact.py -t -l ${LOGGING_LEVEL} -i ${IN_FILE_1} -o ${OUT_FILE_1} ${OUT_FILE_2}

# csv2html -o test.html test/test.csv