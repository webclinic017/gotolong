#!/bin/sh

DEBUG_LEVEL=0

BANK=icici-bank


# dividends data
IN_DIR=$PROJ_PROFILE_DATA_LOC/bank-txn-data
OUT_DIR=$PROJ_PROFILE_REPORTS_LOC/dividend-reports

IN_FILE_AMFI=$PROJ_DATA_LOC/amfi-data/amfi-data-mcap.csv
IN_FILE_ALIASES=${IN_DIR}/nach-aliases/nach-company-ticker-aliases.csv


for FY in fy1617 fy1718 fy1819 all
do

      if [[ "${FY}" == "all" ]]; then
        stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/*/${BANK}/OpTransactionHistory-*.csv
	IN_FILE_1=${IN_DIR}/*/${BANK}/OpTransactionHistory-*.csv
      else
        stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/${FY}/${BANK}/OpTransactionHistory-${FY}.csv
	IN_FILE_1=${IN_DIR}/${FY}/${BANK}/OpTransactionHistory-${FY}.csv
      fi

      OUT_FILE_0=$OUT_DIR/${FY}/${FY}-name_map.csv
      OUT_FILE_1=$OUT_DIR/${FY}/${FY}-name_only.csv
      OUT_FILE_2=$OUT_DIR/${FY}/${FY}-sort_name.csv
      OUT_FILE_3=$OUT_DIR/${FY}/${FY}-sort_frequency.csv
      OUT_FILE_4=$OUT_DIR/${FY}/${FY}-sort_amount.csv

      dividend_invoke.py ${DEBUG_LEVEL} ${IN_FILE_AMFI} ${IN_FILE_ALIASES} ${OUT_FILE_0} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${IN_FILE_1}
done
