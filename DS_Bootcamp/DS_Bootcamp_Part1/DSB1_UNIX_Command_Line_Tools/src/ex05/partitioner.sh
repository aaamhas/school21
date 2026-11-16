#!/bin/sh
tail -n +2 ../ex03/hh_positions.csv | awk -F, '{ print $2 }' | cut -d'T' -f1 | tr -d '"' | sort | uniq | while read -r date; do
    head -1 ../ex03/hh_positions.csv > "$date.csv"
    grep "$date" ../ex03/hh_positions.csv >> "$date.csv"
done