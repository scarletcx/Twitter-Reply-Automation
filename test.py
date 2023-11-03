import requests,os
import random

proxies_file = 'proxies.txt'
def load_reply_texts(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
proxy_list = load_reply_texts(proxies_file)

test_url = 'http://api64.ipify.org?format=json'

def test_proxies(proxy_list):
        proxy_string = random.choice(proxy_list)
        server, port, username, password = proxy_string.split(':')
        try:
            os.environ['http_proxy'] = f"http://{username}:{password}@{server}:{port}"
 
            response = requests.get(test_url)
            if response.status_code == 200:
                print(f"Proxy {proxy_string} is working. Your IP is {response.json()['ip']}")
            else:
                print(f"Proxy {proxy_string} is not working. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Proxy {proxy_string} encountered an error: {str(e)}")

test_proxies(proxy_list)
