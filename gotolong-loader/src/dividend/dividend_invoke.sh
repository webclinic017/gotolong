#!/bin/sh

LOGGING_LEVEL=INFO

CONFIG_GLOBAL_DATA_LOC=`python -m config global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m config global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

BANK=icici-bank

# dividends data
IN_BANK=$CONFIG_PROFILE_DATA_LOC/bank-txn-data/${BANK}
IN_DIR=${IN_BANK}/out-csv
OUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/dividend-reports

IN_FILE_AMFI="$CONFIG_GLOBAL_DATA_LOC/amfi-data/amfi-data-mcap.csv"
IN_FILE_ALIASES=$CONFIG_GLOBAL_DATA_LOC/nach-data/nach-aliases.csv


# excluded all : as it doesn't work on windows
# for FY in fy1617 fy1718 fy1819 fy1920 all
# for FY in all 
for FY in fy1617 fy1718 fy1819 fy1920 fy2021 all
do
    mkdir -p ${OUT_DIR}/${FY}

    if [[ "${FY}" == "all" ]]; then
        #stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/*/OpTransactionHistory-*.csv
	    IN_FILE_BANK_STMT=${IN_DIR}/*/${BANK}-stmt-*.csv
    else
        #stmt-clean/bank-txn-stmt-clean.sh stmt-clean/*legends*.txt ${IN_DIR}/${FY}/OpTransactionHistory-${FY}.csv
	    IN_FILE_BANK_STMT=${IN_DIR}/${FY}/${BANK}-stmt-${FY}.csv
    fi

    OUT_FILE_0=$OUT_DIR/${FY}/${FY}-name_map.csv
    OUT_FILE_1=$OUT_DIR/${FY}/${FY}-name_only.csv
    OUT_FILE_2=$OUT_DIR/${FY}/${FY}-sort_name.csv
    OUT_FILE_3=$OUT_DIR/${FY}/${FY}-sort_frequency.csv
    OUT_FILE_4=$OUT_DIR/${FY}/${FY}-sort_amount.csv
    OUT_FILE_5=$OUT_DIR/${FY}/${FY}-monthly_dividend.csv
    OUT_FILE_6=$OUT_DIR/${FY}/${FY}-comp_monthly_dividend.csv
    OUT_FILE_7=$OUT_DIR/${FY}/${FY}-missing-nach-aliases.csv

    if test ! -e ${IN_FILE_1}
    then
        echo "error: file doesn't exist : ${IN_FILE_1}"
    fi

    python dividend.py -t -l ${LOGGING_LEVEL} -i ${IN_FILE_BANK_STMT} -a ${IN_FILE_ALIASES} -o ${OUT_FILE_0} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5} ${OUT_FILE_6} ${OUT_FILE_7}

done
