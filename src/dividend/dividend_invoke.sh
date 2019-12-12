#!/bin/sh

DEBUG_LEVEL=1

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


BANK=icici-bank


# dividends data
IN_BANK=$CONFIG_PROFILE_DATA_LOC/bank-txn-data/${BANK}
IN_DIR=${IN_BANK}/out-csv
OUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/dividend-reports

IN_FILE_AMFI="$CONFIG_DATA_LOC/amfi-data/amfi-data-mcap.csv"
IN_FILE_ALIASES=${IN_BANK}/nach-aliases/nach-company-ticker-aliases.csv


# excluded all : as it doesn't work on windows
# for FY in fy1617 fy1718 fy1819 fy1920 all
for FY in fy1617 fy1718 fy1819 fy1920 all
do
    mkdir -p ${OUT_DIR}/${FY}

    if [[ "${FY}" == "all" ]]; then
        #stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/*/OpTransactionHistory-*.csv
	IN_FILE_1=${IN_DIR}/*/OpTransactionHistory-*.csv
    else
        #stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/${FY}/OpTransactionHistory-${FY}.csv
	IN_FILE_1=${IN_DIR}/${FY}/OpTransactionHistory-${FY}.csv
    fi

    OUT_FILE_0=$OUT_DIR/${FY}/${FY}-name_map.csv
    OUT_FILE_1=$OUT_DIR/${FY}/${FY}-name_only.csv
    OUT_FILE_2=$OUT_DIR/${FY}/${FY}-sort_name.csv
    OUT_FILE_3=$OUT_DIR/${FY}/${FY}-sort_frequency.csv
    OUT_FILE_4=$OUT_DIR/${FY}/${FY}-sort_amount.csv
    OUT_FILE_5=$OUT_DIR/${FY}/${FY}-monthly_dividend.csv

    if test ! -e ${IN_FILE_1}
    then
        echo "error: file doen't exist : ${IN_FILE_1}"
    fi

    python dividend_invoke.py ${DEBUG_LEVEL} ${IN_FILE_AMFI} ${IN_FILE_ALIASES} ${OUT_FILE_0} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${IN_FILE_1}
done
