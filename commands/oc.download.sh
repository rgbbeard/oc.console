#!/bin/bash
base="$(dirname $(readlink -f $0))"

pod=$(cat "$base/../.currpod")
from=''
to=''

while [[ $# -gt 0 ]]; do
     if [[ "$1" == --* ]]; then
          param="${1#--}"
          value="$2"

          case "$param" in
               pod)
                    if [ "$value" == "last-used" ]; then
                         echo -e "No POD specified, using the last-entered POD\n"
                    else
                         pod="$value"
                    fi
                    ;;
               from)
                    from="$value"
                    ;;
               to)
                    to="$value"
                    ;;
               *)
                    echo "Unknown parameter: $param"
                    ;;
          esac

          shift 2
     else
          echo "Invalid parameter format: $1"
          shift
     fi
done

if [[ -z "$pod" ]]; then
     echo "No POD available for download"
     exit
else
     read -p "This POD will be used to download your file \"$pod\", continue?(Yes/No)" answer

     shopt -s nocasematch

     if [[ "$answer" == "no" || "$answer" == "n" ]]; then
          echo -e "Exiting..\n"
          exit
     fi
fi


if [[ -z "$from" ]]; then
     echo "Empty 'from' parameter"
     exit
fi

if [[ -z "$to" ]]; then
     echo "Empty 'to' parameter"
     exit
fi

# TODO: add local file existence

# download the file
oc rsync $pod:"$from" "$to"
