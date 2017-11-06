#!/bin/bash

#install haproxy
yum -y install haproxy

#configure consul
cd /usr/local/bin
wget https://releases.hashicorp.com/consul/1.0.0/consul_1.0.0_linux_amd64.zip
wget https://releases.hashicorp.com/consul-template/0.19.4/consul-template_0.19.4_linux_amd64.zip
unzip consul-template_0.19.4_linux_amd64.zip
unzip consul_1.0.0_linux_amd64.zip
rm -rf consul-template_0.19.4_linux_amd64.zip
rm -rf consul_1.0.0_linux_amd64.zip
useradd -m consul
usermod -aG sudo consul
mkdir -p /etc/consul.d/client
mkdir /var/consul
chown consul: /var/consul
cd /home/consul
su consul
curl -o consul_server.py https://raw.githubusercontent.com/jerrin92/airavata-django-portal/load-balancing/LoadBalancer/Consul/client/consul_client.py
curl -o haproxy.conf.ctmpl https://raw.githubusercontent.com/jerrin92/airavata-django-portal/load-balancing/LoadBalancer/ha-proxy/consul-template/haproxy.conf.ctmpl
/usr/bin/python /home/consul/consul_client.py
nohup consul agent -enable-script-checks -config-dir /etc/consul.d/client &
sudo consul-template -consul-addr `ifconfig eth0 | grep -w inet | awk {'print $2'}` -template /home/consul/haproxy.conf.ctmpl:/etc/haproxy/haproxy.cfg -log-level=debug

