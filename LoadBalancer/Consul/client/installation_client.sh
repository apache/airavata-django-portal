#!/bin/bash

cd /usr/local/bin
wget https://releases.hashicorp.com/consul/1.0.0/consul_1.0.0_linux_amd64.zip
unzip consul_1.0.0_linux_amd64.zip
rm -rf consul_1.0.0_linux_amd64.zip
useradd -m consul
usermod -aG sudo consul
mkdir -p /etc/consul.d/client
mkdir /var/consul
chown consul: /var/consul
cd /home/consul
curl -o consul_server.py https://raw.githubusercontent.com/jerrin92/airavata-django-portal/load-balancing/LoadBalancer/Consul/client/consul_client.py
/usr/bin/python consul_client.py
su consul
consul agent -enable-script-checks -config-dir /etc/consul.d/client
