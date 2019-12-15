#!/bin/sh

DEBUG_LEVEL=1

CONFIG_SRC_LOC=`python -m config src`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

# To be invoked from following folder with a layout of in-xls and out-csv
# D:\GoogleDrive\my_personal_pack\invest\Equity\icici-bank-txn-data

IN_FILE_DIR=$CONFIG_PROFILE_DATA_LOC/bank-txn-data

#local_repo_root=/d/GoogleDrive/my_github/GitHub
#local_repo_name="gotolong"
debug_level=1

in_dir=in-xls
out_dir=out-csv

for bank in icici-bank sbi-bank hdfc-bank
do
    echo processing bank ${bank}

    cd $IN_FILE_DIR/${bank}

    for fy_dir in `ls ${in_dir}`
    do
	    if test -d ${in_dir}/${fy_dir}
	    then
		    mkdir -p ${out_dir}/${fy_dir}/
            fi

            if test $bank = "icici-bank" -o 'sbi-bank' -o ${bank} = 'hdfc-bank'
            then
                in_file=${in_dir}/${fy_dir}/${bank}-stmt-${fy_dir}.xls
		        out_file=${out_dir}/${fy_dir}/${bank}-stmt-${fy_dir}.csv
            else
		        echo "unknown bank" : $bank
            fi


            echo processing ${fy_dir}

	    python  "${CONFIG_SRC_LOC}/bank-stmt-txn-parser/bank_stmt_txn_xls_to_csv.py" ${bank} ${in_file} ${out_file} ${debug_level}

    done

done
