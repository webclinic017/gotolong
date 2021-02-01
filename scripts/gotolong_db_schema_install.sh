#!/bin/sh

if test $# -lt 1
then
  echo "usage: $0 <mysql | pgsql> <create | import>  <default | db_conn_info>"
  echo "usage: $0 mysql create"
  echo "usage: $0 mysql import"
  echo "usage: $0 pgsql import default"
  exit 1
fi

DB_TYPE=$1
DB_COMMAND=$2
DB_CONN_INFO=$3

# add following to PATH
# C:\Program Files\MariaDB 10.5\bin'

DB_NAME=$(python -m gotolong.config.config_ini db_name)
DB_USER=$(python -m gotolong.config.config_ini db_user)
DB_PASS=$(python -m gotolong.config.config_ini db_pass)

DB_SCHEMA_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_schema.sql
DB_DUMP_SQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump.sql
PG_DB_DUMP_PSQL=${GOTOLONG_DATA}/db/${DB_NAME}_dump_pg.psql

# case statement - valid and invalid command

case "${DB_TYPE}" in
  "mysql" | "pgsql" )
    echo "Valid db_type ${DB_TYPE}"
    ;;
 *)
    echo "Invalid db_type ${DB_TYPE}"
    exit 1
    ;;
esac

case "${DB_COMMAND}" in
  "create" | "import" )
    echo "Valid command ${DB_COMMAND}"
    ;;
 *)
    echo "Invalid command ${DB_COMMAND}"
    exit 1
    ;;
esac


if test ${DB_TYPE} == "mysql"
then

  if test "${DB_COMMAND}" == "create"
  then
    # create schema
    mysql -u${DB_USER} -p${DB_PASS} "${DB_NAME}" < "${DB_SCHEMA_SQL}"
    # mysqldump --no-data -uroot -proot gotolong > ${GOTOLONG_DATA}/db/gotolong_schema.sql
  elif test "${DB_COMMAND}" == "import"
  then
    # full db
    mysql -u${DB_USER} -p${DB_PASS} "${DB_NAME}" < "${DB_DUMP_SQL}"
  fi

fi # mysql

if test ${DB_TYPE} == "pgsql"
then

  if test "${DB_COMMAND}" == "create"
  then
        # create just db name
        PGPASSWORD=${DB_PASS} dropdb -U postgres "${DB_NAME}"
        PGPASSWORD=${DB_PASS} createdb -U postgres "${DB_NAME}"
  elif test "${DB_COMMAND}" == "import"
  then
    # DB connection information

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

fi # pgsql