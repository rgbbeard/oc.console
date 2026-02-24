#!/bin/bash
base="$(dirname $(readlink -f $0))"

echo -en "\033]0;oc.console\a"

function cmdexists() {
    command -v "$1" > /dev/null 2>&1
    return $?
}

if cmdexists "python3" ; then
	python3 "$base/oc.console.py"
elif cmdexists "python"; then
	python "$base/oc.console.py"
else
	echo "Unable to start"
fi
