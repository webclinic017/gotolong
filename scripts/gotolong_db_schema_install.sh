#!/bin/sh

if test $# -lt 1
then
  echo "usage: $0 create_mysql | import_mysql | import_pgsql"
  exit 1
fi

COMMAND=$1

# add following to PATH
# C:\Program Files\MariaDB 10.5\bin'

DB_NAME=$(python -m gotolong.config.config_ini db_name)
DB_USER=$(python -m gotolong.config.config_ini db_user)
DB_PASS=$(python -m gotolong.config.config_ini db_pass)

DB_SCHEMA_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_schema.sql
DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump.sql
PG_DB_DUMP_PSQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump_pg.psql

# case statement - valid and invalid command

case "${COMMAND}" in
  "create_mysql" | "import_mysql" | "import_pgsql" )
    echo "Valid command ${COMMAND}"
    ;;
 *)
    echo "Invalid command ${COMMAND}"
    exit 1
    ;;
esac


if test "${COMMAND}" == "create_mysql"
then
  # create schema
  mysql -u${DB_USER} -p${DB_PASS} "${DB_NAME}" < "${DB_SCHEMA_SQL}"
  # mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_DATA}/db/gotolong_schema.sql
fi

if test "${COMMAND}" == "import_mysql"
then
  # full db
  mysql -u${DB_USER} -p${DB_PASS} "${DB_NAME}" < "${DB_DUMP_SQL}"
fi

# PostgreSQL (password: root)
# pg_

if test "${COMMAND}" == "import_pgsql"
then
  # DB connection information
  DB_CONN_INFO=$2

  if test -z "${DB_CONN_INFO}"
  then
    echo "usage: $0 ${COMMAND} <db_conn_info | default>"
    exit 1
  fi

  if test "${DB_CONN_INFO}" == "default"
  then
    DB_CONN_INFO="dbname=${DB_NAME} host=localhost port=5432 user=postgres password=${DB_PASS}"
    echo "using local db conn information" ${DB_CONN_INFO}
  fi

  psql "${DB_CONN_INFO}" < "${PG_DB_DUMP_PSQL}"

  # pg_restore
  # psql -U postgres -d "${DB_NAME}" -f "${PG_DB_DUMP_PSQL}"
  # for windows command line, use
  # set PGPASSWORD=root
  # psql ...
  # set PGPASSWORD=
fi
