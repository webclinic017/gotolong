#!/bin/sh

if test -n "${GOTOLONG_DEBUG_LEVEL}"
then
    DEBUG_LEVEL=${GOTOLONG_DEBUG_LEVEL}
else
    DEBUG_LEVEL=1
fi


CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

# figure this out automatically
IN_FILE_1=$CONFIG_DATA_LOC/nse-data/nse-52w-hl.csv
OUT_FILE_1=$CONFIG_REPORTS_LOC/nse-reports/nse-reports-52w-hl.csv
OUT_FILE_2=$CONFIG_REPORTS_LOC/nse-reports/nse-reports-52w-hl.txt

# python amfi_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE} --out_files ${OUT_FILE_1}
python ftwhl_invoke.py -t -d ${DEBUG_LEVEL} -i ${IN_FILE_1}  -o ${OUT_FILE_1} ${OUT_FILE_2}

# csv2html -o test.html test/test.csv
