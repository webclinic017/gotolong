#!/bin/sh

for TARGET in plan demat dividend review-dividend tbd
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done
