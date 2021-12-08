#!/usr/bin/env bash
help(){
	echo "SciELO Usage COUNTER - Sort and dedup script"
	echo "Please, inform:"
	echo "   1. The input file (parameter -i)"
	echo "   2. The output file (parameter -o)"
	echo ""
	echo "For example:"
	echo ""
	echo "   sort_uniq.sh -i 2018-06-03.unsorted.tsv -o 2018.06.03.tsv"
	echo ""
}

run(){
	UNSORTED_FILE=$1;
	SORTED_FILE=$2;

    echo "[Processando] $UNSORTED_FILE";
    echo "[Gravando] $SORTED_FILE";
    sort -r -t $'\t' -k 4 $UNSORTED_FILE | uniq > $SORTED_FILE;
}

while getopts i:o: opts; do
	case ${opts} in
		# Arquivo de saída (IP ordenado por ordem alfabética e sem linhas duplicadas)
      	o) SORTED_FILE=${OPTARG} ;;

		# Arquivo de entrada
		i) UNSORTED_FILE=${OPTARG} ;;
	esac
done

if [[ -z "$SORTED_FILE" || -z "$UNSORTED_FILE" ]]
	then
		help;
		exit;
	else
		run $UNSORTED_FILE $SORTED_FILE;
fi
