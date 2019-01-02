#!/bin/sh

DEBUG_LEVEL=0

# gather stats
IN_FILE_YEAR=$PROJ_PROFILE_REPORTS_LOC/demat-reports/stats_year_output.csv
IN_FILE_QTR=$PROJ_PROFILE_REPORTS_LOC/demat-reports/stats_qtr_output.csv

# draw plots
# online
demat_plot.py online ${IN_FILE_YEAR}

# offline
# OUT_FILE_PLOT=$PROJ_PROFILE_REPORTS_LOC/demat-reports/stats_year_output.png
#demat_plot.py offline ${IN_FILE_YEAR} ${OUT_FILE_PLOT}
