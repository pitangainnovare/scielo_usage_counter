#!/usr/bin/env bash

help(){
	echo "SciELO Usage COUNTER - Batch script Parse Log"
	echo "Please, inform:"
	echo "   1. The file MMDB (parameter -m)"
	echo "   2. The file robots (parameter -r)"
	echo "   3. The output directory (parameter -o)"
	echo "   4. The list of files paths (parameter -f)"
	echo "   5. Disable validation (optional, parameter -n)"
	echo ""
	echo "For example:"
	echo ""
	echo "   scripts/batch_parse.sh -m data/map.mmdb -r data/counter-robots.txt -o data -f logs_paths.txt -n"
	echo ""
}

run(){
	FILE_MMDB=$1
	FILE_ROBOTS=$2
	OUTPUT_DIR=$3
	INPUT=$4
	NO_VAL=$5

	for i in $(cat "$INPUT"); do
		LOGFILE=$i
		echo "[Processando] $LOGFILE"

		if [[ "$NO_VAL" == "1" ]]; then
			parse-log -m "$FILE_MMDB" -r "$FILE_ROBOTS" -o "$OUTPUT_DIR" -f "$LOGFILE" --no-validate
		else
			parse-log -m "$FILE_MMDB" -r "$FILE_ROBOTS" -o "$OUTPUT_DIR" -f "$LOGFILE"
		fi
	done
}

NO_VAL=0
while getopts f:m:r:o:n opts; do
	case ${opts} in
    f) INPUT=${OPTARG} ;;
		m) FILE_MMDB=${OPTARG} ;;
    r) FILE_ROBOTS=${OPTARG} ;;
    o) OUTPUT_DIR=${OPTARG} ;;
    n) NO_VAL=1 ;;
	esac
done

if [[ -z "$INPUT" || -z "$FILE_ROBOTS" || -z "$FILE_MMDB"  || -z "$OUTPUT_DIR" ]]; then
	help
	exit
else
	run "$FILE_MMDB" "$FILE_ROBOTS" "$OUTPUT_DIR" "$INPUT" "$NO_VAL"
fi
