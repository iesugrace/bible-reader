#!/bin/bash
# Desc: check the existence of the files
#       listed in the file 'FILE_NAME_LIST'

file=FILE_NAME_LIST
ok=1
while read name
do
    test ! -f $name && echo "missing: $name" && ok=0
done < $file

test $ok = 1 && echo "passed, all files are presented"
