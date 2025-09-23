#!/bin/bash
base="$(dirname $(readlink -f $0))"
. "$base/cmdexists.sh"

echo -en "\033]0;oc.console\a"

function cmdexists() {
	[ -z "$(command -v $1)" ] && echo 1 || echo 0
}

if cmdexists "python3" ; then
	python3 /opt/oc.console/oc.console.py
elif cmdexists "python"; then
	python /opt/oc.console/oc.console.py
else
	echo "Unable to start"
fi
