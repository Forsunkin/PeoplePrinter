import requests
import re

url = 'http://192.168.1.88/'
def get_info():
    r = requests.get(url, allow_redirects=False)
    return r.text


print(get_info())