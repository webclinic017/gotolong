#!/bin/sh

if test $# -lt 2
then
   echo "usage:$0 sector-company-details-units.csv sector-company-units.csv"
   exit 1
fi

# sector-company-details-units
SCDU_FILE=$1
# sector-company-units
SCU_FILE=$2

grep -v -e ',Details'  $SCDU_FILE > $SCU_FILE
