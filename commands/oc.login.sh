#!/bin/bash
base="$(dirname $(readlink -f $0))"

readarray -t lines <<< $(cat $OC_INTERACTIVE_CONSOLE_CREDENTIALS_PATH)

ochost=$(cat "$base/../.ochost");

username="${lines[0]}"
password="${lines[1]}"

if [[ -n $1 ]]; then
	username="$1"
fi

if [[ -n $2 ]]; then
	password="$2"
fi

# TODO: check security issues for eval
eval "{ echo \"$username\"; echo \"$password\"; } | oc login $ochost --insecure-skip-tls-verify"
source "$base/oc.env.sh"