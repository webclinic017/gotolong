#!/usr/bin/env bash

# Store all the files to be moved to download-data

CONFIG_GLOBAL_DATA_LOC=`python -m config global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m config global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

NSE_HOLIDAY_LIST=$CONFIG_GLOBAL_REPORTS_LOC/nse-reports/nse-reports-holiday-list.txt

DOWNLOAD_DIR=${GOTOLONG_HOME}/download

# set defaults
DOWNLOAD_Q=no
REMOVE_Q=yes

if test $# -lt 4;
then
          echo "usage: $0 download <yes|no> remove <yes|no>" 
          echo "usage: $0 download <yes> remove <no>" 
          exit 1
fi        


if [ -n "$2" ]
then
  DOWNLOAD_Q=$2

  if [ "${DOWNLOAD_Q}" != "yes" -a "${DOWNLOAD_Q}" != "no" ];
  then
          echo "usage: $0 download <yes|no> remove <yes|no>" 
          echo "usage: $0 download <yes> remove <no>" 
          exit 1
  fi
fi

if [ -n "$4" ]
then
  REMOVE_Q=$4

  if [ "${REMOVE_Q}" != "yes" -a "${REMOVE_Q}" != "no" ];
  then
          echo "usage: $0 download <yes|no> remove <yes|no>" 
          echo "usage: $0 download <yes> remove <no>" 
          exit 1
  fi
fi

echo "DOWNLOAD_Q = $DOWNLOAD_Q"
echo "REMOVE_Q = $REMOVE_Q"

mkdir -p ${DOWNLOAD_DIR}

if [ "${DOWNLOAD_Q}" == "yes" ];
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
    last_working_day=`date -d "$look_back day ago" +'%d%m'`
    last_working_year=`date -d "$look_back day ago" +'%Y'`

    grep -q $last_working_year $NSE_HOLIDAY_LIST
    if test $? -ne 0;
    then
        echo "please upload the holiday list of 2020"
        exit 1
    fi

    grep -q $last_working_day $NSE_HOLIDAY_LIST
    if test $? -eq 0;
    then
        echo "holiday found... adjusting last working day"
    fi
    # better to check it against holiday list - 2 Oct 2020
    # TODO  - handle entire holiday list - year wise
    # 2nd oct, 15th aug, 26 jan
    if [ $last_working_day == "0210" -o $last_working_day == "2601" -o $last_working_day == "1508" ];
    then
        # Today is Tuesday and holiday on monday (last working date)
        # TODO - handle multiple holidays clubbed together
        if [ $day_or_week -eq 2 ] ; then
            look_back=`expr $look_back + 3`
        else
            look_back=`expr $look_back + 1`
        fi
        last_working_date=`date -d "$look_back day ago" +'%d%m%Y'`
    fi

    if [ -e ${DOWNLOAD_DIR}/nse_fetch_date.txt ]; then
        nse_fetch_date=`cat ${DOWNLOAD_DIR}/nse_fetch_date.txt`
    else
        nse_fetch_date=""
    fi

    # do not fetch again if data has been already fetched for previous day
    if [ ${last_working_date} != "$nse_fetch_date" ] ;
    then
        # 52-week low and high
        # https://archives.nseindia.com/content/CM_52_wk_High_low_${last_working_date}.csv

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
        # unzip will unzip .csv to current directory
        mv cm${LW_DATE_2}bhav.csv ${DOWNLOAD_DIR}
        rm ${DOWNLOAD_DIR}/cm${LW_DATE_2}bhav.csv.zip
        echo ${last_working_date} > ${DOWNLOAD_DIR}/nse_fetch_date.txt
    fi

else
    echo 'skipped download'
fi

# lets experiment in download directory

cd $DOWNLOAD_DIR

if [ -e cm*bhav.csv ];
then
    mv cm*bhav.csv ${CONFIG_GLOBAL_DATA_LOC}/nse-data/nse-bhav.csv
fi

if [ -e CM*.csv ];
then
    mv CM_52_wk_High_low*.csv ${CONFIG_GLOBAL_DATA_LOC}/nse-data/nse-52w-hl.csv
fi

# icicidirect portfolio summary
if [ -e *PortFolioEqtSummary*.csv ];
then
    mv *PortFolioEqtSummary*.csv ${CONFIG_PROFILE_DATA_LOC}/demat-data/icicidirect/demat-summary-data.csv
fi

# icicidirect portfolio all txn
if [ -e *PortFolioEqtAll*.csv ];
then
    mv *PortFolioEqtAll*.csv ${CONFIG_PROFILE_DATA_LOC}/demat-data/icicidirect/demat-txn-data.csv
fi

# trendlyne prefix
TL_SCREEN_NAME="GOTOLONG"
TL_FILE_LIST=trendlyne-flist.txt
> ${TL_FILE_LIST} 
# for tl_filename in `ls *${TL_SCREEN_NAME}*`
ls *${TL_SCREEN_NAME}* | while read tl_filename
do
    echo "tl_filename : ${tl_filename}"

    # NOTE: it still doesn't help
    # add empty new line
    echo "" >> "${tl_filename}"
    echo ${tl_filename} >> ${TL_FILE_LIST} 
done

echo 'suri1'

if [ -s  ${TL_FILE_LIST} ];
then
        echo 'suri2'

        # quite to suppress filename: put header first
        head -q -n 1 *${TL_SCREEN_NAME}*.csv | sort -u > ${CONFIG_GLOBAL_DATA_LOC}/trendlyne-data/trendlyne-data.csv
        # supress header 
        tail -q -n +2 *${TL_SCREEN_NAME}*.csv >> ${CONFIG_GLOBAL_DATA_LOC}/trendlyne-data/trendlyne-data.csv

        # let dummy header be around second time
        # cat *${TL_SCREEN_NAME}*.csv > ${CONFIG_GLOBAL_DATA_LOC}/trendlyne-data/trendlyne-data.csv

        if [ "${REMOVE_Q}" = "yes" ];
        then
            rm *${TL_SCREEN_NAME}*.csv
            rm ${TL_FILE_LIST}
        fi
fi
