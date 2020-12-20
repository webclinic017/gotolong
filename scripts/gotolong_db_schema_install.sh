#!/usr/bin/env bash

if test $# -lt 1
then
  echo "usage: $0 create_mysql | import_mysql | import_pgsql"
  exit 1
fi

COMMAND=$1

cd 'C:\Program Files\MariaDB 10.4\bin'
DB_NAME=`python -m gotolong.config.config_ini db_name`

DB_SCHEMA_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_schema.sql
DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump.sql
PG_DB_DUMP_PSQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump_pg.psql

if test "${COMMAND}" == "create_mysql"
then
  # create schema
  mysql -uroot -proot ${DB_NAME} < ${DB_SCHEMA_SQL}
  # mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_DATA}/db/gotolong_schema.sql
fi

if test "${COMMAND}" == "import_mysql"
then
  # full db
  mysql -uroot -proot ${DB_NAME} < ${DB_DUMP_SQL}
fi

# PostgreSQL (password: root)
# pg_

if test "${COMMAND}" == "import_pgsql"
then
  # pg_restore
  psql -U postgres -d ${DB_NAME} -f ${PG_DB_DUMP_PSQL}
fi