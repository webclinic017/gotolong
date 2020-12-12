#!/bin/sh

# curl https://www.nseindia.com/content/indices/ind_nifty50list.csv
awk -F',' '{print $3}' ind_nifty50list.csv | sort -u | grep -v -e Symbol >  user-nifty-stock-list.csv
