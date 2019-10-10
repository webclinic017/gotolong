#!/usr/bin/env bash

echo files : $*

# replace print ... with print()

for file in $*
do
  perl -p -i -e 's/print (.*)$/print\($1\)/g' $file
  # edit in vi editor
  # :1,$s///g 
done
