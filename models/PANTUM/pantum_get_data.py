import requests
import re

url = 'http://192.168.1.88/index.html'
r1 = r'>(.*)%<'
def get_info():
    page = requests.get(url).text
    toner = re.findall(r1, page)
    return page

print(get_info())