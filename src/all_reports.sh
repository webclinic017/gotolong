#!/bin/sh

# NOTE : removed plan module data

TARGET_LIST=$1

if [ ${TARGET_LIST} = "daily" ];
then

    for TARGET in demat bhav ftwhl phealth
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

else

    # AMFI & ISIN
    for TARGET in amfi isin
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in demat
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in screener trendlyne
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    # nse bhav and 52-w low and high
    for TARGET in bhav ftwhl
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    # assign weights
    for TARGET in global_weight
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in phealth
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in bse
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in bank-stmt-txn-parser dividend
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

    for TARGET in anomaly
    do
      cd $PROJ_SOURCE_LOC/$TARGET
      ./*.sh
    done

fi