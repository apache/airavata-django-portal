#!/bin/bash
source /home/centos/anaconda2/bin/activate py3
cd /home/centos/airavata-django-portal
nohup /home/centos/anaconda2/envs/py3/bin/python manage.py runserver 0.0.0.0:8000 &
source deactivate
cd ~
mkdir -p /var/consul
mkdir -p /etc/consul.d/client
/home/centos/anaconda2/envs/py3/bin/python consul_template.py
nohup /usr/local/bin/consul agent -enable-script-checks -config-dir /etc/consul.d/client &
