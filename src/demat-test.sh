#!/bin/sh

DEBUG_LEVEL=0

demat-test.py ${DEBUG_LEVEL} $PROJ_DATA_LOC/demat-data/demat-txn-hist/*.csv $*
