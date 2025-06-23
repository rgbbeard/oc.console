#!/bin/bash
U=${SUDO_USER:-$(whoami)}
base="$(dirname $(readlink -f $0))"

. "$base/.utils/cmdexists.sh"
. "$base/config.sh"
. "$base/makeexecutable.sh"

# must run as super user
if [ "$(id -u)" != "0" ]; then
   echo "This script must run as root"
   exit 1
fi

if [ ! -d "$installdir" ]; then
   echo -e "Starting installation..\n"
   # copy files into the destination folder
   cp -ir "$base" "$destfolder"

   makeexecutable

   # make all the files executable
   chmod +x "$installdir/commands/*"
   chmod +x "$installdir/oc.console.desktop"
   
   # create start icon
   cp "$installdir/oc.console.desktop" "/usr/share/applications/oc.console.desktop"

   # create desktop icon
   cp "$installdir/oc.console.desktop" "/home/$U/Desktop/oc.console.desktop"
   echo "Installation completed"

   # install python requirements
   if cmdexists python3; then
      python3 -m pip install prompt-toolkit
   elif cmdexists python; then
      python -m pip install prompt-toolkit
   fi
else
   echo "The program is already installed and located in $installdir"
fi
