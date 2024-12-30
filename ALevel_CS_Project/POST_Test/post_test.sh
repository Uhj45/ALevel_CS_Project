#!/bin/bash
cd /home/uhjas
. venv-pwm/bin/activate
cd /home/uhjas/csp
sudo -E env PATH=$PATH /home/uhjas/venv-pwm/bin/python /home/uhjas/csp/POST_Test.py 2>&1 /home/uhjas/csp/POST_Test/post_test.error