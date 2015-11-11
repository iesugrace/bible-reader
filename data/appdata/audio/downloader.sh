#!/bin/bash
# Desc: a convenient script to download files
# and rename and place them appropriately.
# Directory and file names are all numbers
# according to their position.

getdirname() {
    local name
    name=$1
    name=$(sed -r 's/\.mp3$//' <<< "$name")     # remove trailing .mp3
    name=$(sed -r 's/%20[0-9]+$//' <<< "$name") # remove file seq number if any
    name=$(sed -r 's/%20//g' <<< "$name")       # remove remaining spaces (%20)
    name=$(awk "\$2 == \"$name\" {print \$1} " $book_names)
    echo "$name"
}

getfilename() {
    local name
    name=$1
    name=$(sed -r 's/%20/ /g' <<< "$name")  # replace %20 with space
    name=$(awk '{print $NF}' <<< "$name")   # fetch the last part

    # some books has only one chapter, thus no seq number in name
    if ! grep -Eq '^[0-9]+\.mp3$' <<< "$name"; then
        name="1.mp3"
    fi

    name=$(sed -r 's/^0+//' <<< "$name")    # remove leading zero(s)
    echo "$name"
}

url_file=URLs
book_names=BOOK_NAMES_SEQUENCE

while read url
do
    lastpart=$(echo "$url" | awk -F/ '{print $NF}')
    dirname=$(getdirname "$lastpart")
    filename=$(getfilename "$lastpart")
    mkdir -p $dirname
    wget -c "$url" -O "${dirname}/${filename}"
done < $url_file
