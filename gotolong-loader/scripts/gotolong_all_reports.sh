#!/bin/sh

# NOTE : removed plan module data

TARGET_LIST=$1

if [ ${TARGET_LIST} = "daily" ];
then

    for TARGET in demat bhav ftwhl phealth
    do
       ${TARGET}-invoke
      #${TARGET}_invoke.sh
    done

else

    # AMFI & ISIN
    for TARGET in amfi isin
    do
      ${TARGET}_invoke.sh
    done

    for TARGET in demat
    do
      ${TARGET}_invoke.sh
    done

    for TARGET in screener trendlyne
    do
      ${TARGET}_invoke.sh
    done

    # nse bhav and 52-w low and high
    for TARGET in bhav ftwhl
    do
      ${TARGET}_invoke.sh
    done

    # assign weights
    for TARGET in global_weight
    do
      ${TARGET}_invoke.sh
    done

    # corpact uses bse reports
    for TARGET in bse corpact
    do
      ${TARGET}_invoke.sh
    done

    for TARGET in phealth
    do
      ${TARGET}_invoke.sh
    done

    for TARGET in bank-stmt-txn-parser dividend
    do
      ${TARGET}_invoke.sh
    done

    for TARGET in anomaly
    do
      ${TARGET}_invoke.sh
    done

fi