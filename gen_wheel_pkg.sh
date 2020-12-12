#!/usr/bin/env bash

# clean older stuff in build directory
python setup.py clean --all

# check build directory for creating wheel package.
# check dist directory for wheel package
python setup.py bdist_wheel

# first dump the db schema and db dump
gotolong_db_gen.sh

# generate .tar.gz for data
tar -cvf ${PROJECT_ROOT}/dist/gotolong-data.tar data
gzip ${PROJECT_ROOT}/dist/gotolong-data.tar