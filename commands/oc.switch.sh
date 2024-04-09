#!/bin/bash

if [[ -z "$1" ]]; then
	eval "./oc.env.sh"
	oc projects
	exit
fi

oc project "$1"

tmp=$(oc project "$1")
dev=$(echo "$tmp" | grep -E ".*-dev\"")
prod=$(echo "$tmp" | grep -E ".*-prod.*\"")

if [[ -n "$dev" ]]; then
	eval "./oc.env.sh dev"
elif [[ -n "$prod" ]]; then
	eval "./oc.env.sh prod"
fi