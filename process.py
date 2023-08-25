from PeoplePrinter import PeoplePrinter
import requests


ip = 'https://192.168.1.88'

r = requests.get(ip, verify=False)
print(r.history)
