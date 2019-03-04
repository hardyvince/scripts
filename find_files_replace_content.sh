#!/bin/bash

FILES=`\
find a/b/ -type f -name '*.c'; \
find a/c/ -type f -name '*.c'`

for f in $FILES
do
sed -i 's/x/y/g' $f
sed -i 's/x/z/g' $f
done
