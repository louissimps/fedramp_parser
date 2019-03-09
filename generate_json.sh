#!/bin/bash


display_usage() {
  echo
  echo "Usage: $0"
  echo
  echo " -h, --help   Display usage instructions"
  echo " -e, --env  prod,dev"
  echo
}

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
output_file=""
verbose=0

while getopts "h?me:" opt; do
    case "$opt" in
    h|\?)
        display_usage
        exit 0
        ;;
    m)  markdown=1
        ;;
    e)  environment=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "${1:-}" = "--" ] && shift







echo "Creating output dir"
mkdir -p output/

echo "Processing Controls"
python cleanup_csv.py

#shorten the list a little bit
if [[ $environment == "dev" ]]; then
echo "Cutting records way back to avoid build times being really long"

cat output/fedramp_controls.json |  jq '[limit(10;.[])]' > output/controls.json
echo "Created output/controls.json shortened dev version for use in explorer project"
rm -rf output/fedramp_controls.json
else
echo "Created output/controls.json for prod use in explorer project"
mv output/fedramp_controls.json output/controls.json
fi

if [[ $markdown == "1" ]]; then
    echo "Generating fedramp_controls.markdown"
    torsimany output/fedramp_controls.json
fi







