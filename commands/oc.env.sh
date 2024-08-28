#!/bin/bash
base="$(dirname $(readlink -f $0))"

currenv="DEVELOPMENT"

if [[ -n $1 ]]; then
	if [[ "$1" == "dev" ]]; then
		currenv="DEVELOPMENT"
	elif [[ "$1" == "prod" ]]; then
		currenv="PRODUCTION"
	fi

  	# save the current working environment
	echo "$currenv" > "$base/../.currenv"
else
	currenv=$(cat "$base/../.currenv")
fi

echo -e "Currently using environment: $currenv\n"
