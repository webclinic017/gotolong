#!/usr/bin/env bash

FILE=$1

# replace print ... with print()

perl -p -i -e 's/print (.*)$/print\($1\)\$/g' $1

