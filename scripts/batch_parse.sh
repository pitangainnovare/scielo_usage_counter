#!/usr/bin/env bash

set -euo pipefail

help(){
	echo "SciELO Usage COUNTER - Batch script Parse Log"
	echo "Usage: $0 -m <mmdb_file> -r <robots_file> -o <output_dir> -f <input_file_list> [-n]"
	echo ""
	echo "Options:"
	echo "   -m FILE    MMDB file"
	echo "   -r FILE    Robots file"
	echo "   -o DIR     Output directory"
	echo "   -f FILE    File with a list of log file paths to parse"
	echo "   -v         Validate (optional)"
	echo ""
	echo "For example:"
	echo ""
	echo "   $0 -m data/map.mmdb -r data/counter-robots.txt -o data -f logs_paths.txt -v"
	echo ""
}

VAL=0
while getopts ":f:m:r:o:n" opt; do
	case ${opt} in
    f) INPUT=${OPTARG} ;;
		m) FILE_MMDB=${OPTARG} ;;
    r) FILE_ROBOTS=${OPTARG} ;;
    o) OUTPUT_DIR=${OPTARG} ;;
    n) VAL=1 ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      help
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      help
      exit 1
      ;;
	esac
done

if [ -z "${INPUT:-}" ] || [ -z "${FILE_ROBOTS:-}" ] || [ -z "${FILE_MMDB:-}" ] || [ -z "${OUTPUT_DIR:-}" ]; then
	help
	exit 1
fi

# Check if files exist
if [ ! -f "$INPUT" ]; then
    echo "Input file not found: $INPUT" >&2
    exit 1
fi
if [ ! -f "$FILE_MMDB" ]; then
    echo "MMDB file not found: $FILE_MMDB" >&2
    exit 1
fi
if [ ! -f "$FILE_ROBOTS" ]; then
    echo "Robots file not found: $FILE_ROBOTS" >&2
    exit 1
fi
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Output directory not found: $OUTPUT_DIR" >&2
    exit 1
fi

while IFS= read -r LOGFILE || [ -n "$LOGFILE" ]; do
    # Skip empty lines
    if [ -z "$LOGFILE" ]; then
        continue
    fi

    echo "[Processing] $LOGFILE"

    if [ "$VAL" = "0" ]; then
        parse-log -m "$FILE_MMDB" -r "$FILE_ROBOTS" -o "$OUTPUT_DIR" -f "$LOGFILE"
    else
        parse-log -m "$FILE_MMDB" -r "$FILE_ROBOTS" --validate -o "$OUTPUT_DIR" -f "$LOGFILE"
    fi
done < "$INPUT"

echo "Done."
