#!/bin/sh

echo Generate the db schema files
gotolong_db_schema_gen.sh

echo Reset the PG DB remotely
heroku pg:reset --confirm gotolong --app gotolong

export HEROKU_DATABASE_URL=`heroku config:get --app gotolong DATABASE_URL`
echo Install the PG DB remotely
gotolong_db_schema_install.sh pgsql import "${HEROKU_DATABASE_URL}"