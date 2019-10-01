#!/usr/bin/env bash



# get rid of the program name
shift

echo files : $*

# replace print ... with print()

for file in $*
do
  unix2dos $file
  perl -p -i -e 's/print (.*)$/print\($1\)\$/g' $file
done
