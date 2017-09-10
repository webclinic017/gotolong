#!/bin/sh

cat icicidirect-portfolio.txt | awk -F',' '{ if (prev_company != $1) { prev_company=$1; prev_year=0; prev_month=0;printf("%s - %s\n",$1, $2);} year=substr($6,1,4); month=substr($6,6,2); day=substr($6,9,2); if (prev_year != year) { prev_year=year; printf("Year %s\n",year);}  if (prev_month != month) { prev_month=month; printf("\tMonth %s\n",month); } printf("\t\t%s:%s@%s %s\n", $4*$5, $4, $5, $3);   }'
