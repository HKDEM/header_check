import subprocess
 
# Dynamically installs a vulnerable package version of requests
subprocess.run(["pip", "install", "requests==2.24.0"])

import requests
# Use the installed requests
response = requests.get('https://httpbin.org/get')
print(response.json())
