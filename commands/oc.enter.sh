#!/bin/bash
base="$(dirname $(readlink -f $0))"

source "$base/oc.env.sh"

currpod=""

if [[ -n $1 ]]; then
	currpod=$1
  	# save the current working pod
	echo "$1" | tee "$base/../.currpod"
else
	echo -e "No POD specified, oc will now try to check for the last used POD\n"

	currpod=$(cat "$base/../.currpod")

	if [ -z "$currpod" ]; then
		echo -e "No valid POD to enter. Exiting..\n"
		exit
	fi

	echo -e "Found $currpod\n"
fi

echo -e "Entering POD: $currpod\n"

oc rsh "$currpod" bash
