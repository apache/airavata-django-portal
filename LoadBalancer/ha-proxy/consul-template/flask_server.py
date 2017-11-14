from flask import Flask
import json
import re

app = Flask(__name__)
@app.route("/")

def hello():
        serverRegex = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        with open('/etc/haproxy/haproxy.cfg','r') as f:
                content = f.read()
        servers = serverRegex.findall(content)
        return json.dumps(servers)

if __name__ == "__main__":
        app.run()
