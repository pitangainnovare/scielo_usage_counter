#!/usr/bin/env bash
help(){
	echo "SciELO Usage COUNTER - Batch script Generate Pretable"
	echo "Please, inform the directory of logs (parameter -d). For example: "
	echo ""
	echo "   scripts/batch_generate_pretable.sh -d /logs_preprocessed"
	echo ""
}

run(){
	DIR_PREPROCESSED_LOGS=$1;
	echo "[DIR_PREPROCESSED_LOGS] $DIR_PREPROCESSED_LOGS"

	for i in `ls "$DIR_PREPROCESSED_LOGS"`; do
		PPLOG=$DIR_PREPROCESSED_LOGS/$i;

		echo "[Processando] $PPLOG";
		gen_pt \
			-f $PPLOG
	done
}

while getopts d: opts; do
	case ${opts} in
		# Diretório contendo arquivos de log preprocessados
      	d) DIR_PREPROCESSED_LOGS=${OPTARG} ;;
	esac
done

if [[ -z "$DIR_PREPROCESSED_LOGS" ]]
	then
		help;
		exit;
	else
		run $DIR_PREPROCESSED_LOGS;
fi
