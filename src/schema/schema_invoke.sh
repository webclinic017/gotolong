#!/bin/sh

DEBUG_LEVEL=1

CONFIG_DB_SCHEMA_LOC=`python -m config db_schema`

# IN_DB_FILE=${CONFIG_DB_LOC}/equity.db
IN_SCHEMA_FILE=${CONFIG_DB_SCHEMA_LOC}/equity_schema.sql

python schema_invoke.py ${DEBUG_LEVEL} ${IN_SCHEMA_FILE}
# python schema_invoke.py ${DEBUG_LEVEL} ${IN_DB_FILE} ${IN_SCHEMA_FILE}
