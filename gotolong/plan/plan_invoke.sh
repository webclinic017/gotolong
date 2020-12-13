#!/bin/sh

if test -n "${GOTOLONG_DEBUG_LEVEL}"
then
    DEBUG_LEVEL=${GOTOLONG_DEBUG_LEVEL}
else
    DEBUG_LEVEL=0
fi

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

IN_FILE_PLAN=$CONFIG_PROFILE_DATA_LOC/plan-data/plan-data.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-ticker-only.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-sort-units.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-all-holdings.csv
OUT_FILE_4=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-plus-holdings.csv
OUT_FILE_5=$CONFIG_PROFILE_REPORTS_LOC/plan-reports/plan-reports-zero-holdings.csv

#python plan_invoke.py --truncate_table --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
# python plan_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
python plan_invoke.py -d ${DEBUG_LEVEL} -i ${IN_FILE_PLAN} -o ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
