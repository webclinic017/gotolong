#!/usr/bin/env bash

# first dump the db schema and db dump

gotolong_db_gen.sh

# check build directory for creating wheel package.
# check dist directory for wheel package
python setup.py bdist_wheel
