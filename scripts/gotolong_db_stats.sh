#!/usr/bin/env bash

DB_STATS_INPUT=${GOTOLONG_DATA}/db/gotolong_db_stats.sql
DB_STATS_OUTPUT=${GOTOLONG_DATA}/db/gotolong_db_stats.txt

# display in nice tabular format
DISPLAY_FORMAT=--table

if test -e ${DB_STATS_INPUT} ; then
    mysql -uroot -proot ${DISPLAY_FORMAT} < ${DB_STATS_INPUT} > ${DB_STATS_OUTPUT}
else
    echo Error file not found ${DB_STATS_INPUT}
fi

# enforce Heroku free tier limits
gotolong_heorku_limits_check.py