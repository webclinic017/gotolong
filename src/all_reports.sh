#!/bin/sh

# NOTE : removed plan module data

# AMFI & ISIN
for TARGET in amfi isin
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in demat demat-zerodha demat-sum-stat demat-txn-stat
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done

for TARGET in screener trendlyne chealth
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done

for TARGET in weight phealth
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


for TARGET in anomanly
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done
