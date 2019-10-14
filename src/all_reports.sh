#!/bin/sh

# screener target tbd
for TARGET in amfi isin plan weight demat dividend screener anomaly 
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done
