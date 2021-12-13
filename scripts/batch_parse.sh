#!/usr/bin/env bash
help(){
	echo "SciELO Usage COUNTER - Batch script Parse Log"
	echo "Please, inform:"
	echo "   1. The directory of logs or a list of files paths (parameter -i)"
	echo "   2. The file MMDB (parameter -m)"
	echo "   3. The file robots (parameter -r)"
	echo "   4. The output directory (parameter -o)"
	echo ""
	echo "For example:"
	echo ""
	echo "   scripts/batch_parse.sh -i logs/apache -m data/map.mmdb -r data/counter-robots.txt -o data"
	echo ""
	echo "   or"
	echo ""
	echo "   scripts/batch_parse.sh -i logs_paths.txt -m data/map.mmdb -r data/counter-robots.txt -o data"
	echo ""
}

run(){
	INPUT=$1;
	FILE_MMDB=$2;
	FILE_ROBOTS=$3;
	OUTPUT_DIR=$4;

	if [[ -d $INPUT ]]; then
		CMD='ls';
	elif [[ -f $INPUT ]]; then
		CMD='cat';
	else
		echo "Invalid value for parameter -i"
		exit 1
	fi

	for i in `$CMD "$INPUT"`; do
		LOGFILE=$DIR_LOGS/$i;

		echo "[Processando] $LOGFILE";
		parse -f $LOGFILE -m "$FILE_MMDB" -r "$FILE_ROBOTS" -o "$OUTPUT_DIR";
	done
}

while getopts i:m:r:o: opts; do
	case ${opts} in
		# Diretório de arquivos de log ou arquivo indicando caminhos dos arquivos a serem processados
      	i) INPUT=${OPTARG} ;;

		# Arquivo de mapas em formato mmdb
		m) FILE_MMDB=${OPTARG} ;;

		# Arquivo de bots em formato txt
	  	r) FILE_ROBOTS=${OPTARG} ;;

		# Diretório de resultados
		o) OUTPUT_DIR=${OPTARG} ;;
	esac
done

if [[ -z "$INPUT" || -z "$FILE_ROBOTS" || -z "$FILE_MMDB"  || -z "$OUTPUT_DIR" ]]
	then
		help;
		exit;
	else
		run $INPUT $FILE_MMDB $FILE_ROBOTS $OUTPUT_DIR;
fi
