#!/bin/sh

if test $# -lt 1
then
   echo "usage: $0 bank-stmt.csv"
   echo $* 
   exit 1
fi

LEGENDS_FILE=$1

shift

for BANK_TXN_STMT_FILE in $*
do

# Skip Legends  like MMT, RTGS, NEFT using grep
cat $BANK_TXN_STMT_FILE | grep -v -f ${LEGENDS_FILE} | grep -v -e ':Int.Pd:' -e 'BY CASH' -e ',,,,,,,,,' > ${BANK_TXN_STMT_FILE}.new

mv ${BANK_TXN_STMT_FILE}.new ${BANK_TXN_STMT_FILE}

done
