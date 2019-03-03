#!/bin/bash

if [[ $1 == "-m" ]]; then
    CREATE_MARKDOWN=1
fi
# \?) echo "generate_json [-m] optional m flag to generate markdown file";;
# esac
# done

echo "Creating output dir"
mkdir -p output/

echo "Processing Controls"
python cleanup_csv.py


if [[ $CREATE_MARKDOWN == "1" ]]; then
    echo "Generating fedramp_controls.markdown"
    torsimany output/fedramp_controls.json
fi



