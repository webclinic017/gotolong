#!/bin/sh

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

#ECHO=echo

# Usage
# Requires plan file and dividend data

PLAN_NAME=${CONFIG_PROFILE_REPORTS_LOC}/plan-reports/plan-reports-ticker-only.csv

OUT_DIR=${CONFIG_PROFILE_REPORTS_LOC}/plan-dividend-reports
mkdir -p ${OUT_DIR}

for DIV_YEAR in fy1516 fy1617 fy1718 fy1819 fy1920 all
do
    DIV_NAME=${CONFIG_PROFILE_REPORTS_LOC}/dividend-reports/${DIV_YEAR}/${DIV_YEAR}-name_only.csv

    # display unique plan only entries (column 1)
    $ECHO comm -23 ${PLAN_NAME} ${DIV_NAME} > ${OUT_DIR}/plan_only-${DIV_YEAR}.csv
done
