#!/bin/bash

echo "Extracting Tables"
python extract_table.py

echo "Make csv dir and move files"
rm -rf csv &&  mkdir csv && mv fedramp_*.csv csv/

echo "Convert CSV"
python convert.py


