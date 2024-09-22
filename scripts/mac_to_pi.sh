#!/bin/bash

filename=${1}
tarfile="${2}.tar.gz"
echo "${tarfile} ${filename}"
#tar -czvf "${tarfile}" ${filename}
tar -czvf "${tarfile}" FlaskTest.py templates static PWM_Fan.py
scp -i ~/.ssh/raspberrypi.rsa ./${tarfile} uhjas@192.168.1.71:

