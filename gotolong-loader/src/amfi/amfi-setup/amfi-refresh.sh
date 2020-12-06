#!/bin/sh

if test $# -lt 2
then
    echo "usage: $0 curl"
fi 


# year number
CUR_YEAR=`date +%Y`
PREV_YEAR=`expr $CUR_YEAR - 1`

# month number
CUR_MONTH=`date +%m`

# curl works on both windows and Linux
if test "$1" = "curl"
then
    ECHO=
else
    ECHO=echo
fi

CONFIG_GLOBAL_DATA_LOC=`python -m config global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m config global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


AMFI_DATA_DIR=$CONFIG_GLOBAL_DATA_LOC/amfi-data/

cd $AMFI_DATA_DIR


OUT_DIR=in-xls

# new format
# https://www.amfiindia.com/Themes/Theme1/downloads/Average%20Market%20Capitalization%20of%20Listed%20Companies%20during%20Jan%20-%20Jun%202020_Final.xlsx

for YEAR in ${PREV_YEAR} ${CUR_YEAR}
do
# use curl -o instead of wget -O
# -O has different meaning for curl and last segment of url is used as filename
$ECHO curl -o ${OUT_DIR}/${YEAR}/amfi-mcap-jan-jun-${YEAR}.xlsx https://www.amfiindia.com/Themes/Theme1/downloads/Avg.%20Market%20Capitalization%20of%20listed%20companies%20during%20-Jan-June%20${YEAR}.xlsx

$ECHO curl -o ${OUT_DIR}/${YEAR}/amfi-mcap-jul-dec-${YEAR}.xlsx https://www.amfiindia.com/Themes/Theme1/downloads/Avg.%20Market%20Capitalization%20of%20listed%20companies%20during%20-Jul-Dec%20${YEAR}.xlsx
done
