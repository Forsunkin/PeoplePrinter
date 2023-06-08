import requests
import re

first_ip = '192.168.1.38'

url_toner = f'http://{first_ip}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
url_couner = f'http://{first_ip}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'





# Получить количество отпечатаных листов
# Дописать логику передачи ip
def get_counter(ip):
    url_couner = f'http://{ip}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    
    rst = requests.get(url_couner)
    printer_total = re.findall(r".*printertotal = \('(\d*)'\)", rst.text)           # получить отпечатанные листы
    copy_total = re.findall(r".*copytotal = \('(\d*)'\)", rst.text)                 # получить сканы
    result = int(printer_total[0]) + int(copy_total[0])                             # получить тотал
    return result

# Получить отсток тоннера
# Дописать логику передачи ip
def get_toner(ip):
    url_toner = f'http://{ip}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
    
    rst = requests.get(url_toner)
    toner = re.findall(r".*parseInt\('(\d*)',10\)\)", rst.text)                     # получить остаток тонера
    result = toner [0]
    return result


print(get_counter('192.168.1.38'))
print(get_toner('192.168.1.38'))

