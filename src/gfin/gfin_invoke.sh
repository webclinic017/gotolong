#!/bin/sh

if test -n "${GOTOLONG_DEBUG_LEVEL}"
then
    DEBUG_LEVEL=${GOTOLONG_DEBUG_LEVEL}
else
    DEBUG_LEVEL=0
fi

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

OUT_DIR_1=$CONFIG_REPORTS_LOC/gfin-reports
OUT_FILE_1=${OUT_DIR_1}/gfin-reports.csv

mkdir -p ${OUT_DIR_1}

#python plan_invoke.py --truncate_table --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
# python plan_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
python gfin_invoke.py -d ${DEBUG_LEVEL} -o ${OUT_FILE_1}
