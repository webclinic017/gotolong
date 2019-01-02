#!/bin/sh

CUR_YEAR=`date +%Y`
PREV_YEAR=`expr $CUR_YEAR - 1`

for YEAR in ${PREV_YEAR} ${CUR_YEAR}
do
wget -O amfi-mcap-jan-june-${YEAR}.xlsx https://www.amfiindia.com/Themes/Theme1/downloads/Avg.%20Market%20Capitalization%20of%20listed%20companies%20during%20-Jan-June%20${YEAR}.xlsx

wget -O amfi-mcap-jul-dec-${YEAR}.xlsx https://www.amfiindia.com/Themes/Theme1/downloads/Avg.%20Market%20Capitalization%20of%20listed%20companies%20during%20-Jul-Dec%20${YEAR}.xlsx
done
