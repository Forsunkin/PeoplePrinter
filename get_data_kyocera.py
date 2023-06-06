import requests
url = 'http://192.168.1.38/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
import re

# def get_data(url):
#     r = requests.get(url)
#     print(r.text)

# get_data(url)

f = open("exemple_kyocera.txt", "r")
data = f.read()

def parse_data(obj):
    printer_total = re.findall(r".*printertotal = \('(\d*)'\)", obj)
    copy_total = re.findall(r".*copytotal = \('(\d*)'\)", obj)
    result = int(printer_total[0]) + int(copy_total[0])
    return result


print(parse_data(data))