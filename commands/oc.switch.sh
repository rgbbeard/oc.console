#!/bin/bash
base="$(dirname $(readlink -f $0))"

if [[ -z "$1" ]]; then
	source "$base/oc.env.sh"
	oc projects
	exit
fi

oc project "$1"

tmp=$(oc project "$1")
dev=$(echo "$tmp" | grep -E ".*-dev\"")
prod=$(echo "$tmp" | grep -E ".*-prod.*\"")

if [[ -n "$dev" ]]; then
	eval "$base/oc.env.sh dev"
elif [[ -n "$prod" ]]; then
	eval "$base/oc.env.sh prod"
fi