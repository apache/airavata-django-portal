import json
import os
import subprocess


if __name__ == '__main__':
        bashCommand = "ifconfig eth0 | grep -w inet | awk {'print $2'}"
        privateIP = subprocess.check_output(['bash','-c',bashCommand]).rstrip()
        bashCommand = "curl ipinfo.io/ip"
        publicIP = subprocess.check_output(['bash','-c',bashCommand]).rstrip()
        serviceEndPoint = "http://"+publicIP+":8000"
        #print(serviceEndPoint)
        hostname = subprocess.check_output(['bash','-c','hostname']).rstrip()
        #print(hostname)
        with open('/home/consul/serverlist.txt') as reader:
                servers = reader.readlines()
                servers = [x.strip('\n') for x in servers]

        with open('/etc/consul.d/client/data.json','w') as outfile:
                json.dump({
                "bind_addr":privateIP,
                "datacenter": "dc1",
                "data_dir": "/var/consul",
                "log_level": "INFO",
                "enable_syslog": bool(1),
                "enable_debug": bool(1),
                "node_name": hostname,
                "server": bool(0),
                "rejoin_after_leave": bool(1),
                "retry_join": servers,
                "client_addr": "0.0.0.0"
                },outfile,indent=4)
