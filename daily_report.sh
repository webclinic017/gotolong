#!/usr/bin/env bash

# to invoke report
export GOTOLONG_EXCEL=excel

./download_move.sh download yes remove yes 

./src/all_reports.sh daily
