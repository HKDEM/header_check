import subprocess
import sys

# Force install of a vulnerable version of requests
def install_vulnerable_dependency():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests==2.24.0"])

def get_data():
    import requests
    url = "https://httpbin.org/get"
    response = requests.get(url)
    print(response.json())

if __name__ == "__main__":
    install_vulnerable_dependency()
    get_data()
