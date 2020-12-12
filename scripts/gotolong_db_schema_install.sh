#!/usr/bin/env bash

cd 'C:\Program Files\MariaDB 10.4\bin'
DB_NAME=`python -m gotolong_config db_name`

DB_SCHEMA_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_schema.sql
DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump.sql

# create schema
mysql -uroot -proot ${DB_NAME} < ${DB_SCHEMA_SQL}

# full db
mysql -uroot -proot ${DB_NAME} < ${DB_DUMP_SQL}

# mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_DATA}/db/gotolong_schema.sql
