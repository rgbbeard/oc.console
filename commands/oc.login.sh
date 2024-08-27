#!/bin/bash
base="$(dirname $(readlink -f $0))"

readarray -t lines <<< $(cat $OC_INTERACTIVE_CONSOLE_CREDENTIALS_PATH)

ochost=$(cat "$base/../.ochost");

username="${lines[0]}"
password="${lines[1]}"

# TODO: check security issues for eval
eval "{ echo \"$username\"; echo \"$password\"; } | oc login $ochost --insecure-skip-tls-verify"
source "$base/oc.env.sh"