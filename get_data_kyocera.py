import requests
import re
import datetime

# Получить количество отпечатаных листов
def get_counter(ip):
    url_counter = f'http://{ip}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    
    rst = requests.get(url_counter)
    printer_total = re.findall(r".*printertotal = \('(\d*)'\)", rst.text)           # получить отпечатанные листы
    copy_total = re.findall(r".*copytotal = \('(\d*)'\)", rst.text)                 # получить сканы
    result = int(printer_total[0]) + int(copy_total[0])                             # получить тотал
    return result

# Получить отсток тоннера
def get_toner(ip):
    url_toner = f'http://{ip}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
    
    rst = requests.get(url_toner)
    toner = re.findall(r".*parseInt\('(\d*)',10\)\)", rst.text)                     # получить остаток тонера
    result = int(toner[0])
    return result


print(get_counter('192.168.1.78'))
print(get_toner('192.168.1.78'))

# Нужна функция которая принимает ip возвращает dict для сохранения в базу
def get_values(ip):
    values = {"ip": ip, "datatime":, }
    get_counter(ip)
    get_toner(ip)


