#!/bin/bash

currenv="DEVELOPMENT"

if [[ -n $1 ]]; then
	if [[ "$1" == "dev" ]]; then
		currenv="DEVELOPMENT"
	elif [[ "$1" == "prod" ]]; then
		currenv="PRODUCTION"
	fi

	echo "$currenv" | tee currenv
else
	currenv=$(cat "./currenv")
fi

echo -e "Currently using environment: $currenv\n"