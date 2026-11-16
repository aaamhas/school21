#!/bin/sh

head -1 ../ex03/hh_positions.csv > tmp_output

for file in *.csv; do
    tail -n +2 "$file" >> tmp_output
done

mv tmp_output hh_concatenated.csv