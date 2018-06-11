#!/bin/sh

DEBUG_LEVEL=0

demat_prep_invoke.py ${DEBUG_LEVEL} $PROJ_DATA_LOC/demat-data/demat-txn-hist/*PortFolioEqtSummary*.csv $* > $PROJ_DATA_LOC/demat-data/demat-txn-hist/quick-portfolio.csv
