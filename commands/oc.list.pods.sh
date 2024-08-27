#!/bin/bash
base="$(dirname $(readlink -f $0))"

source "$base/oc.env.sh"
command="oc get pod"

if [ -z "$1" ]
	then eval "$command"
	exit
else
	eval "$command | grep $1"
	exit
fi
