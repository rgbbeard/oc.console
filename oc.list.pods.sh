#!/bin/bash

eval "./oc.env.sh"
command="oc get pod"

if [ -z "$1" ]
	then eval $command
	exit
else
	eval "$command |grep $1"
	exit
fi
