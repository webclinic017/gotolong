#!/bin/sh

DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

IN_DIR=$PROJ_PROFILE_DATA_LOC/bank-txn-data/
OUT_DIR=$PROJ_PROFILE_REPORTS_LOC/dividend-reports/
for FY in fy1617 fy1718 all
do
  for SORT_TYPE in name_only sort_name sort_amount sort_frequency 
  do
      if [[ "${FY}" == "all" ]]; then
     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${IN_DIR}/*/OpTransactionHistory-*.csv > ${OUT_DIR}/${FY}/${FY}-${SORT_TYPE}.csv
      else
     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${IN_DIR}/${FY}/OpTransactionHistory-${FY}.csv > ${OUT_DIR}/${FY}/${FY}-${SORT_TYPE}.csv
      fi
  done
done

