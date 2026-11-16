#!/bin/sh

head -1 ../ex02/hh_sorted.csv > hh_positions.csv

tail -n +2 ../ex02/hh_sorted.csv | while read -r line; do
    name=$(echo "$line" | awk 'BEGIN { FPAT = "([^,]+)|(\"[^\"]*\")" } { gsub(/^"|"$/, "", $3); print $3 }')

    position=$(echo "$name" | grep -oE "Junior|Middle|Senior" | tr '\n' '/' | sed 's/\/$//')

    if [ -z "$position" ]; then
        position="-"
    fi

    echo "$line" | awk -v newval="$position" 'BEGIN { FPAT = "([^,]+)|(\"[^\"]*\")"; OFS="," } { $3 = "\"" newval "\""; print }'
done >> hh_positions.csv