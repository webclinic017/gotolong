#!/bin/sh

# AMFI & ISIN
for TARGET in amfi isin
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in demat-idirect demat-zerodha demat-txn-stat
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in bank-stmt-txn-parser dividend
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in screener trendlyne chealth gfin
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in anomanly
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in bse
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done


for TARGET in plan weight
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done