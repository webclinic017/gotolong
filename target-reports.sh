#!/bin/sh


OUT_TYPE=out_plain
SORT_TYPE=sort_name
SUMMARY_TYPE=summary_no
DEBUG_LEVEL=0

FY=all

./target-stats.py ${OUT_TYPE} ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ./sample-data/target-hist/${FY}/*-target-units.csv  > ./reports/targets/${FY}/${FY}-name_only.txt
