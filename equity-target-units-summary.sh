#!/bin/sh

# README

# Input Template (equity-target-units.csv) file
# Ignore first 10 lines
# Each entry template
#Industry,Sub Industry, Company,Planned Units,Planned Value,Current Value,TBD Value,TBD Units,TBD %,Last Date,,,,,,,,,

if test $# -lt 1
then
   echo "usage: $0 equity-target-units-input.csv"
   exit 1
fi
 
f=$1
lines=`wc -l $f|awk '{print $1}'`
lines=`expr $lines - 10`
tail -${lines} $f | sort -t, > sort.csv

awk -F "," '
BEGIN {
      prev_industry="";
      prev_sub_industry="";
      ind_total=0;
      sub_ind_total=0;
      portfolio_total=0;
      printf("------------------------------------\n\n");
      printf(": Portfolio Distribution : \n");
      printf("------------------------------------\n\n");
  }

  {
    if (prev_industry != $1) { 
            if (NR != 1)
            {
              printf("\n** %s (%d) \n\n", prev_sub_industry, sub_ind_total); 
              printf("\n%s (%d)\n", prev_industry, ind_total); 
              printf("------------------------------------\n\n");
            }
            portfolio_total+=ind_total;
            prev_industry=$1;
            prev_sub_industry=$2;
            ind_total=$6; 
            sub_ind_total=$6; 
     }
     else {
           ind_total+=$6;

           if (prev_sub_industry != $2) {
              printf("\n** %s (%d) \n\n", prev_sub_industry, sub_ind_total); 
              portfolio_total+=sub_ind_total;
              prev_sub_industry=$2;
              sub_ind_total=$6; 
            }
            else {
               sub_ind_total+=$6;
            }
     }
     printf("%s (%s) | ", $3, $6); 
  }

END {  
       printf("\n** %s (%d) \n\n", prev_sub_industry, sub_ind_total); 
       printf("\n%s (%d)\n", prev_industry, ind_total); 
       printf("------------------------------------\n\n");
       printf(": Portfolio Value %d :\n", portfolio_total); 
       printf("------------------------------------\n\n");
    } ' sort.csv
