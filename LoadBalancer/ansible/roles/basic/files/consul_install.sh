wget https://releases.hashicorp.com/consul/1.0.1/consul_1.0.1_linux_amd64.zip
unzip consul_1.0.1_linux_amd64.zip
rm -rf consul_1.0.1_linux_amd64.zip
echo 'export PATH=$PATH:/home/consul' >> /home/consul/.bashrc
