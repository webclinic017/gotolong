#!/bin/sh

DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

IN_DIR=$PROJ_PROFILE_DATA_LOC/bank-txn-data
BANK=icici-bank
OUT_DIR=$PROJ_PROFILE_REPORTS_LOC/dividend-reports
for FY in fy1617 fy1718 all
do
  for SORT_TYPE in name_only sort_name sort_amount sort_frequency 
  do
      if [[ "${FY}" == "all" ]]; then
        bank-txn-stmt-clean.sh ${IN_DIR}/*/${BANK}/OpTransactionHistory-*.csv

     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${IN_DIR}/*/${BANK}/OpTransactionHistory-*.csv > ${OUT_DIR}/${FY}/${FY}-${SORT_TYPE}.csv
      else
        bank-txn-stmt-clean.sh ${IN_DIR}/${FY}/${BANK}/OpTransactionHistory-${FY}.csv
     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ${IN_DIR}/${FY}/${BANK}/OpTransactionHistory-${FY}.csv > ${OUT_DIR}/${FY}/${FY}-${SORT_TYPE}.csv
      fi
  done # SORT_TYPE
done # FY

