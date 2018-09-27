#!/bin/sh

DATA_SFUND_FILE=$PROJ_PROFILE_DATA_LOC/sfund-data/sfund-data.csv
REPORTS_SFUND_FILE=$PROJ_PROFILE_REPORTS_LOC/sfund-demat-sync-reports/sfund-names.txt
 
awk -F "," '
{ if (start_printing) { for (i=4; i<=NF;i++) {print $i} } }
/Category/ { if ($1 == "Category") {start_printing=1} } 
' ${DATA_SFUND_FILE} | sort -u | grep -v -e '#'  | sed '/^$/d' > ${REPORTS_SFUND_FILE}

