import time

import requests
import re


def get_3040(ip_address):
    url = f'http://{ip_address}/dvcinfo/dvcconfig/DvcConfig_Config.htm'

    headers = {'Cookie': 'rtl=0; css=0',
               'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}



    page_code_info = requests.get(url, headers=headers)

    mac = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[175\]\+" :",(".{17}")', page_code_info.text)[0]
    model = re.findall(r".*model = '(.*)'", page_code_info.text)[0]                # получть Модель
    host_name = re.findall(r".*hostName = '(.*)'", page_code_info.text)[0]         # получить HostName



def get_data_printer(ip_address):
    headers = {'Cookie': 'rtl=0; css=0',
               'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}
    try:
        url = f'http://{ip_address}'
        response = requests.get(url)
        if 'KYOCERA' in response.text:
            if 'DeepSleep.htm' in response.text:
                print('Попытка разбудить')
                time.sleep(5)
                requests.get('http://192.168.1.33/esu/DeepSleepApply.htm', headers=headers)
                print(response.text)
            else:
                print('123')
        elif 'HP LaserJet' in response.text:
            pass
        else:
            print(ip_address, ' - Неверный ip')
    except requests.exceptions.ConnectionError:
            print(ip_address, ' - ConnectTimeout')

ip_adress = '192.168.1.33'

get_data_printer(ip_adress)