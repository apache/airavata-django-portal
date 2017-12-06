import json
import os
import subprocess

if __name__ == '__main__':
        bashCommand = "ifconfig eth0 | grep -w inet | awk {'print $2'}"
        privateIP = subprocess.check_output(['bash','-c',bashCommand]).rstrip()
        hostname = subprocess.check_output(['bash','-c','hostname']).rstrip()
        with open('/home/consul/serverlist.txt') as reader:
                servers = reader.readlines()
                servers = [x.replace('\n',':8301') for x in servers]
    
        with open('/etc/consul.d/server/data.json','w') as outfile:
                json.dump({
                "client_addr":"0.0.0.0",
                "bind_addr":privateIP,
                "datacenter": "dc1",
                "data_dir": "/var/consul",
                "log_level": "INFO",
                "enable_syslog": bool(1),
                "enable_debug": bool(1),
                "node_name": hostname,
                "server": bool(1),
                "bootstrap_expect":3,
                "leave_on_terminate": bool(0),
                "skip_leave_on_interrupt": bool(1),
                "rejoin_after_leave": bool(1),
                "retry_join":servers
                },outfile,indent=4)
