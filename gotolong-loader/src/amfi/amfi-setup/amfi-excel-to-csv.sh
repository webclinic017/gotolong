#!/bin/sh

# To be invoked from following folder with a layout of in-xls and out-csv
# D:\GoogleDrive\my_personal_pack\invest\Equity\icici-bank-txn-data

local_repo_root=/d/GoogleDrive/my_github/GitHub
local_repo_name="gotolong"
debug_level=1

CONFIG_GLOBAL_DATA_LOC=`python -m config global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m config global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


AMFI_DATA_DIR=$CONFIG_GLOBAL_DATA_LOC/amfi-data/

cd $AMFI_DATA_DIR

in_dir=in-xls
out_dir=out-csv

# moved bank to up level
#bank=icici-bank

for fy_dir in `ls ${in_dir}`
do

  echo processing ${fy_dir}

  # 
  if test -d ${in_dir}/${fy_dir}
  then
    mkdir -p ${out_dir}/${fy_dir}/

    for half_year in 1 2
    do

      if test "$half_year" -eq 1
      then
        hy_duration=jan-jun
      else
        hy_duration=jul-dec
      fi

      filename=amfi-mcap-${hy_duration}-${fy_dir}
      in_file=${in_dir}/${fy_dir}/${filename}.xlsx
      out_file=${out_dir}/${fy_dir}/${filename}.csv

      # create only new .csv files : do not touch existing files
      if test -e $in_file  ; then
        if test ! -e $out_file ; then
          python  "${local_repo_root}/${local_repo_name}/src/amfi/amfi_excel_to_csv.py" ${in_file} ${out_file} ${debug_level}
        fi
      fi

    done

  fi

done
