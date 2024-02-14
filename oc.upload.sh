# oc cp ~{directory_locale_file_da_uploadare) nome_pod_in_esecuzione(da RSH):{directory_dentro_il_container}

pod=''
from=''
to=''

# get parameters
while [ $# -gt 0 ]
do
     case "$1" in
          --pod)
               pod="$2"
          shift;;
     esac
     case "$3" in
          --from)
               from="$4"
          shift;;
     esac
     case "$5" in
          --to)
               to="$6"
          shift;;
     esac
done

if [[ -z "$pod" ]]; then
     echo "Empty pod name"
     exit
fi
if [[ -z "$from" ]]; then
     echo "Empty 'from' parameter"
     exit
fi
if [[ -z "$to" ]]; then
     echo "Empty 'to' parameter"
     exit
fi