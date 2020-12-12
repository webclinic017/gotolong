#!/bin/sh

# NOTE : removed plan module data

TARGET_LIST=$1

if [ ${TARGET_LIST} = "daily" ];
then

    for TARGET in bhav ftwhl demat phealth
    do
      gotolong_${TARGET}_invoke
      #${TARGET}_invoke.sh
    done

    if test -n "${GOTOLONG_EXCEL}"
    then
        CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong_config profile_reports`
        PHEALTH_OUT_FILE=${CONFIG_PROFILE_REPORTS_LOC}/phealth-reports/phealth-reports.csv
        excel ${PHEALTH_OUT_FILE} &
    fi

else

    # AMFI & ISIN
    for TARGET in amfi isin
    do
      gotolong_${TARGET}_invoke
      #${TARGET}_invoke.sh
    done

    for TARGET in screener trendlyne
    do
      ${TARGET}_invoke.sh
    done

    # nse bhav and 52-w low and high
    for TARGET in bhav ftwhl
    do
      gotolong_${TARGET}_invoke
      # ${TARGET}_invoke.sh
    done

    # assign weights (global-weight)
    for TARGET in gweight
    do
      gotolong_${TARGET}_invoke
    done

    for TARGET in bse
    do
      ${TARGET}_invoke.sh
    done

    # corpact uses bse reports
    for TARGET in corpact
    do
      gotolong_${TARGET}_invoke
    done

    for TARGET in demat
    do
      gotolong_${TARGET}_invoke
      # ${TARGET}_invoke.sh
    done

    for TARGET in phealth
    do
      gotolong_${TARGET}_invoke
    done

    for TARGET in bank-stmt-txn-parser dividend
    do
      ${TARGET}_invoke.sh
    done

    # anomaly-invoke.sh
    # generate DB statistics
    gotolong_db_stats.sh
fi