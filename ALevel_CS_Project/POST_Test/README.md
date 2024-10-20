## POST Test
This folder contains scripts to setup Raspberry Pi to run python tests on power up and reboot

* A shell script called `post_test.sh` launches the python script in its virtual environment
* A service script called `csp_project_post_test.service` is registered in systemd

### Bash Launch Script
This script will launch the python script into a virtual environment 
```angular2html
#!/bin/bash
cd /home/uhjas
. venv-pwm/bin/activate
cd /home/uhjas/csp
/home/uhjas/venv-pwm/bin/python /home/uhjas/csp/POST_Test.py 2>&1 /home/uhjas/csp/POST_Test/post_test.error
```

### SystemD service script

```angular2html
[Unit]
Description=CSP Project Post Test
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/uhjas/csp/POST_Test/post_test.sh 2>&1 /home/uhjas/csp/POST_Test/post_test.log
WorkingDirectory=/home/uhjas
User=uhjas

[Install]
WantedBy=multi-user.target
```

### Register Service script in systemd
Use the following commands to register the service script. This step only needs to be done once when Raspberry Pi is setup
```angular2html
$ sudo chmod a+x /home/uhjas/csp/POST_Test/post_test.sh
$ sudo cp /home/uhjas/csp/POST_Test/csp_project_post_test.service /lib/systemd/system
$ sudo chmod 644 /lib/systemd/system/csp_project_post_test.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable csp_project_post_test.service
$ sudo systemctl status csp_project_post_test.service
```
