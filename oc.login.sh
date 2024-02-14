#!/bin/bash

readarray -t lines <<< $(cat $OC_INTERACTIVE_CONSOLE_CREDENTIALS_PATH)

ochost="https://api.os02.ocp.cineca.it:6443";
using_old_server=0

# get parameters
while [ $# -gt 0 ]
do
     case "$1" in
          --vecchia-paas)
               ochost="https://osmaster-prod-1.cineca.it:8443/"
               using_old_server=1
			echo "USING OLD PAAS SERVER"
          shift;;
     esac
done

username="${lines[0]}"
password="${lines[1]}"

eval "{ echo \"$username\"; echo \"$password\"; } | oc login $ochost --insecure-skip-tls-verify"

# not used anymore
if [[ using_old_server -eq 0 ]]; then
  eval "./oc.switch.sh miur-legacy-dev"
fi
