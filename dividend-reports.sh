#!/bin/sh

for FY in fy1617 fy1718 
do
  for SORT_TYPE in sort_name sort_amount sort_frequency 
  do
     icici-dividend-stats.py ./sample-data/bank-txn-hist/${FY}/OpTransactionHistory-${FY}.csv csv ${SORT_TYPE} > reports/dividends/${FY}-${SORT_TYPE}.csv
  done
done

