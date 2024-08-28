#!/bin/bash
# where am i?
base="$(dirname $(readlink -f $0))"
optdir="/opt/oc.console/"

# must run as super user
if [ "$(id -u)" != "0" ]; then
   echo "This script must run as root"
   exit 1
fi

if [ ! -d $optdir ]; then
   echo -e "Starting installation..\n"
   # copy files into the destination folder
   cp -ir "$base" "/opt/"
   # make all the files executable
   chmod +x "$optdir/commands/*"
   chmod +x "$optdir/oc.console.desktop"
   # create start icon
   cp "$optdir/oc.console.desktop" "/usr/share/applications/oc.console.desktop"
   # create desktop icon
   cp "$optdir/oc.console.desktop" "/home/$USER/Desktop/oc.console.desktop"
   echo "Installation completed"

   # install python requirements
   python3 -m pip install prompt-toolkit
else
   echo "The program is already installed and located in /opt/oc.console"
fi
