#!/usr/bin/env bash

# Store all the files to be moved to download-data

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

DOWNLOAD_DIR=${PROJECT_ROOT}/download-data

if [ -n "$1" ]
then
  CMD=$1
else
  CMD="move"
fi

echo "CMD = $CMD"

if [ "${CMD}" == "download" ];
then
    day_or_week=`date +%w`
    if [ $day_or_week == 1 ] ; then
      look_back=3
    elif [ $day_or_week == 0 ] ; then
      look_back=2
    else
      look_back=1
    fi

    # 11082020 - 11 aug 2020
    last_working_date=`date -d "$look_back day ago" +'%d%m%Y'`

    # 52-week low and high
    # https://archives.nseindia.com/content/CM_52_wk_High_low_${last_working_date}.csv

    DOWNLOAD_DIR=${PROJECT_ROOT}/download-data

    curl --output ${DOWNLOAD_DIR}/CM_52_wk_High_low_${last_working_date}.csv https://archives.nseindia.com/content/CM_52_wk_High_low_${last_working_date}.csv

    # Bhavcopy for CMP
    # https://archives.nseindia.com/content/historical/EQUITIES/2020/AUG/cm12AUG2020bhav.csv.zip

    # last working date, year, month
    # month must be converted to upper case
    LW_DATE_2=`date -d "$look_back day ago" +'%d%b%Y'|tr '[:lower:]' '[:upper:]'`
    LW_YEAR=`date -d "$look_back day ago" +'%Y'`
    LW_MONTH=`date -d "$look_back day ago" +'%b'|tr '[:lower:]' '[:upper:]'`
    BHAV_FILE=cm-bhav.csv.zip
    curl --output  ${DOWNLOAD_DIR}/cm${LW_DATE_2}bhav.csv.zip https://archives.nseindia.com/content/historical/EQUITIES/${LW_YEAR}/${LW_MONTH}/cm${LW_DATE_2}bhav.csv.zip
    unzip ${DOWNLOAD_DIR}/cm${LW_DATE_2}bhav.csv.zip
    rm ${DOWNLOAD_DIR}/cm${LW_DATE_2}bhav.csv.zip
fi

# lets experiment in download directory

cd $DOWNLOAD_DIR

if [ -e cm*bhav.csv ];
then
    mv cm*bhav.csv ${CONFIG_DATA_LOC}/nse-data/nse-bhav.csv
fi

if [ -e CM*.csv ];
then
    mv CM_52_wk_High_low*.csv ${CONFIG_DATA_LOC}/nse-data/nse-52w-hl.csv
fi

# icicidirect portfolio summary
if [ -e *Summary*.csv ];
then
    mv *PortFolioEqtSummary*.csv ${CONFIG_PROFILE_DATA_LOC}/demat-data/icicidirect/demat-summary-data.csv
fi

# trendlyne prefix
TL_SCREEN_NAME="GOTOLONG"
TL_FILE_FOUND="no"
for tl_filename in `ls *${TL_SCREEN_NAME}*`
do
    TL_FILE_FOUND="yes"

    if [ "${TL_FILE_FOUND}" = "yes" ];
    then
        break
    fi

done

if [ "${TL_FILE_FOUND}" = "yes" ];
then
        cat *${TL_SCREEN_NAME}*.csv > ${CONFIG_DATA_LOC}/trendlyne-data/trendlyne-data.csv
        rm *${TL_SCREEN_NAME}*.csv
fi