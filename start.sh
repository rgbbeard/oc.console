#!/bin/bash
base="$(dirname $(readlink -f $0))"
. "$base/.utils/cmdexists.sh"

echo -en "\033]0;oc.console\a"

if [[ $(cmdexists "python3") -eq 0 ]]; then
	python3 /opt/oc.console/oc.console.py
elif [[ $(cmdexists "python") -eq 0 ]]; then
	python /opt/oc.console/oc.console.py
else
	echo "Unable to start"
fi
