#!/bin/sh

# curl https://www.nseindia.com/content/indices/ind_nifty500list.csv
awk -F',' '{print $3}' ind_nifty500list.csv | sort -u | grep -v -e Symbol >  user-nse500-ticker-list.csv
