#!/usr/bin/env bash
help(){
	echo "SciELO Usage COUNTER - Batch script Parse Log"
	echo "Please, inform:"
	echo "   1. The file MMDB (parameter -m)"
	echo "   2. The file robots (parameter -r)"
	echo "   3. The output directory (parameter -o)"
	echo "   4. The list of files paths (parameter -f)"
	echo ""
	echo "For example:"
	echo ""
	echo "   scripts/batch_parse.sh -m data/map.mmdb -r data/counter-robots.txt -o data -f logs_paths.txt"
	echo ""
}

run(){
	FILE_MMDB=$1;
	FILE_ROBOTS=$2;
	OUTPUT_DIR=$3;
	INPUT=$4;

	for i in `cat "$INPUT"`; do
		LOGFILE=$i;

		echo "[Processando] $LOGFILE";
		parse-log -m "$FILE_MMDB" -r "$FILE_ROBOTS" -o "$OUTPUT_DIR" file -f $LOGFILE;
	done
}

while getopts f:m:r:o: opts; do
	case ${opts} in
		# Diretório de arquivos de log ou arquivo indicando caminhos dos arquivos a serem processados
      	f) INPUT=${OPTARG} ;;

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
		run $FILE_MMDB $FILE_ROBOTS $OUTPUT_DIR $INPUT;
fi
