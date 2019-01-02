#!/bin/sh

for TARGET in plan demat tbd
do
  cd $PROJ_SOURCE_LOC/$TARGET
  ./*.sh
done
