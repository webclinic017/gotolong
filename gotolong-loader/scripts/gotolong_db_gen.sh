#!/usr/bin/env bash

cd 'C:\Program Files\MariaDB 10.4\bin'
DB_NAME=gotolong

# only schema
mysqldump --no-data -uroot -proot ${DB_NAME} > ${GOTOLONG_HOME}/data/db/${DB_NAME}_schema.sql

# full db
mysqldump -uroot -proot ${DB_NAME} > ${GOTOLONG_HOME}/data/db/${DB_NAME}_dump.sql

# mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_HOME}/db/gotolong_schema.sql
