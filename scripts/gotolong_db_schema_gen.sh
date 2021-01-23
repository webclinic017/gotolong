#!/bin/sh

# cd 'C:\Program Files\MariaDB 10.5\bin'
DB_NAME=$(python -m gotolong.config.config_ini db_name)
DB_USER=$(python -m gotolong.config.config_ini db_user)
DB_PASS=$(python -m gotolong.config.config_ini db_pass)

DB_SCHEMA_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_schema.sql
DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump.sql
PG_DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump_pg.sql
PG_DB_DUMP_PSQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump_pg.psql

# only schema
mysqldump --no-data -u${DB_USER} -p${DB_PASS} ${DB_NAME} > ${DB_SCHEMA_SQL}

# full db
mysqldump -u${DB_USER} -p${DB_PASS} ${DB_NAME} > ${DB_DUMP_SQL}

# compat : pgsql
mysqldump -u${DB_USER} -p${DB_PASS} --compatible=postgresql --default-character-set=utf8 ${DB_NAME} > ${PG_DB_DUMP_SQL}

python -m gotolong.mysql-postgresql-converter.db_converter ${PG_DB_DUMP_SQL}  ${PG_DB_DUMP_PSQL}

# mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_DATA}/db/gotolong_schema.sql

# generate statistics and check limits
gotolong_db_stats.sh