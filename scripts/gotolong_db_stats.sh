#!/bin/sh

DB_STATS_INPUT=${GOTOLONG_DATA}/db/gotolong_db_stats.sql
DB_STATS_OUTPUT=${GOTOLONG_DATA}/db/gotolong_db_stats.txt

# display in nice tabular format
DISPLAY_FORMAT=--table

DB_NAME=$(python -m gotolong.config.config_ini db_name)
DB_USER=$(python -m gotolong.config.config_ini db_user)
DB_PASS=$(python -m gotolong.config.config_ini db_pass)

if test -e ${DB_STATS_INPUT} ; then
    mysql -u${DB_USER} -p${DB_PASS} ${DISPLAY_FORMAT} < ${DB_STATS_INPUT} > ${DB_STATS_OUTPUT}
else
    echo Error file not found ${DB_STATS_INPUT}
fi

# enforce Heroku free tier limits
python -m gotolong.database.db_heroku_limits_check