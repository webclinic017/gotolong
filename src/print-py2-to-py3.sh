#!/usr/bin/env bash

echo files : $*

# replace print ... with print()

for file in $*
do
  unix2dos $file
  perl -p -i -e 's/print (.*)$/print\($1\)/g' $file
  dos2unix $file
  perl -p -i -e 's///g' $file
done
