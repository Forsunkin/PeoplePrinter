# from src.PeoplePrinter import PeoplePrinter
#
#
# ip = '192.168.1.36'
# printer = PeoplePrinter(ip)
# print(printer.full_info())

import requests
headers = {'Cookie': 'rtl=0; css=0',
               'Referer': f"http://192.168.1.33/esu/DeepSleepApply.htm"}
url = 'http://192.168.1.33/esu/set.cgi'
r = requests.post(url, headers=headers, data='submit001=%D0%9F%D1%83%D1%81%D0%BA&okhtmfile=DeepSleepApply.htm&func=wakeup')
'''Рабочие пробуждение'''