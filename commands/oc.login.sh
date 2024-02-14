#!/bin/bash

readarray -t lines <<< $("cat $OC_INTERACTIVE_CONSOLE_CREDENTIALS_PATH")

ochost=$(cat "../ochost");

username="${lines[0]}"
password="${lines[1]}"

# TODO: check security issues for eval
eval "{ echo \"$username\"; echo \"$password\"; } | oc login $ochost --insecure-skip-tls-verify"
