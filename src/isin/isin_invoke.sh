#!/bin/sh

DEBUG_LEVEL=0

IN_FILE_BSE=$PROJ_DATA_LOC/isin-data/bse-500.csv
IN_FILE_NSE=$PROJ_DATA_LOC/isin-data/nse-500.csv
OUT_FILE_1=$PROJ_DATA_LOC/isin-data/isin-data-phase-1.csv

isin_invoke.py ${DEBUG_LEVEL} ${IN_FILE_BSE} ${IN_FILE_NSE} ${OUT_FILE_1}
