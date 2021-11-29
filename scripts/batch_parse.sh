#!/usr/bin/env bash
help(){
	echo "SciELO Usage COUNTER - Batch script Parse Log"
	echo "Please, inform:"
	echo "   1. The directory of logs (parameter -d)"
	echo "   2. The file MMDB (parameter -m)"
	echo "   3. The file robots (parameter -r)"
	echo ""
	echo "For example:"
	echo ""
	echo "   scripts/batch_parse.sh -d /logs/apache -m /data/map.mmdb -r /data/counter-robots.txt"
	echo ""
}

run(){
	LOGFILE=$1;
	FILE_MMDB=$2;
	FILE_ROBOTS=$3;

	for i in `ls "$DIR_LOGS"`; do
		LOGFILE=$DIR_LOGS/$i;

		echo "[Processando] $LOGFILE";
		parse -f $LOGFILE -m "$FILE_MMDB" -r "$FILE_ROBOTS"; 
	done
}

while getopts d:m:r: opts; do
	case ${opts} in
		# Diretório contendo arquivos de log a serem processados
      	d) DIR_LOGS=${OPTARG} ;;

		# Arquivo de mapas em formato mmdb
		m) FILE_MMDB=${OPTARG} ;;
	  
		# Arquivo de bots em formato txt
	  	r) FILE_ROBOTS=${OPTARG} ;;	
	esac
done

if [[ -z "$DIR_LOGS" || -z "$FILE_ROBOTS" || -z "$FILE_MMDB" ]]
	then
		help;
		exit;
	else
		run $DIR_LOGS $FILE_MMDB $FILE_ROBOTS;
fi
