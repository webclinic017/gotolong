#!/bin/sh

if test $# -lt 1
then
   echo "usage: $0 bank-stmt.csv"
   echo $* 
   exit 1
fi

for BANK_TXN_STMT_FILE in $*
do

cat $BANK_TXN_STMT_FILE | grep -v -e 'NEFT-' -e ':Int.Pd:' -e 'MMT/' -e 'RTGS-' -e 'BY CASH' -e ',,,,,,,,,' > ${BANK_TXN_STMT_FILE}.new

mv ${BANK_TXN_STMT_FILE}.new ${BANK_TXN_STMT_FILE}

done
