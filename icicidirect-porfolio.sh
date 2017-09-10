#!/bin/sh

# Download ICICIDirect porfolio (all transaction ) in .csv format in icicidirect-equity-txns.csv
# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,

cat icicidirect-equity-txns.csv | awk -F',' '{ if (prev_company != $1) { prev_company=$1; prev_year=0; prev_month=0; printf("%s - %s\n",$1, $2);} tdate=$13; year=substr(tdate,8,4); month=substr(tdate,4,3); day=substr(tdate,1,2); if (prev_year != year) { prev_year=year; printf("Year %s\n",year);}  if (prev_month != month) { prev_month=month; printf("\t%s\n",month); } printf("\t\t%s:%s@%s %s\n",$5*$6, $5, $6, $4);   }'


