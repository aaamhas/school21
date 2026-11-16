#!/bin/sh
echo '"name","count"' > hh_uniq_positions.csv
tail -n +2 ../ex03/hh_positions.csv | awk -F, '{ print $2 }' | sort | uniq -c | awk '{ print $2","$1 }' | sort -t, -k2 -n -r >> hh_uniq_positions.csv