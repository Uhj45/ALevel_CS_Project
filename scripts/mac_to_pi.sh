#!/bin/bash
USAGE="mac_to_pi.sh <archive_filename>"
ARCHIVE_NAME=${1}
# variable to store the location of archive file and names the achrive using the first argument in the script 
TARFILE="installation_package/${ARCHIVE_NAME}.tar.gz"
echo "${TARFILE}"
 
# copies files into an archive called ${tarfile}
# includes all files in current folder and excludes the ones in installation_package and venv-csproject
tar -czvf "${TARFILE}" --exclude venv-csproject --exclude installation_package --exclude sqlite/ *

# copies the archive file onto the raspberry pi into the csp folder 
scp -i ~/.ssh/raspberrypi.rsa ./${TARFILE} uhjas@192.168.1.71:csp/tars

# Remotely untars the archive on the raspberry pi in the csp folder 
ssh -i ~/.ssh/raspberrypi.rsa uhjas@192.168.1.71 "tar -xzvf ~/csp/tars/${ARCHIVE_NAME}.tar.gz -C ~/csp" 
