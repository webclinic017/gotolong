#!/bin/sh

DEBUG_LEVEL=0
SUMMARY_TYPE=summary_yes

for FY in fy1617 fy1718 all
do
  for SORT_TYPE in sort_name sort_amount sort_frequency 
  do
      if [[ "${FY}" == "all" ]]; then
     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ./sample-data/bank-txn-hist/*/OpTransactionHistory-*.csv > reports/dividends/${FY}/${FY}-${SORT_TYPE}.csv
      else
     	dividend-stats.py out_csv ${SORT_TYPE} ${SUMMARY_TYPE} ${DEBUG_LEVEL} ./sample-data/bank-txn-hist/${FY}/OpTransactionHistory-${FY}.csv > reports/dividends/${FY}/${FY}-${SORT_TYPE}.csv
      fi
  done
done

