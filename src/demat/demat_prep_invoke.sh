#!/bin/sh

DEBUG_LEVEL=0

OUT_DIR=$PROJ_DATA_LOC/demat-data/

demat_prep_invoke.py ${DEBUG_LEVEL} $PROJ_DATA_LOC/demat-data/*PortFolioEqtSummary*.csv $OUT_DIR/portfolio-phase-1.csv $OUT_DIR/portfolio-phase-2.csv $OUT_DIR/portfolio-phase-3.csv $OUT_DIR/portfolio-phase-4.csv
