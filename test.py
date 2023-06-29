import requests
from get_data_kyocera import get_prints_toner_kyocera
from get_data_hp import get_prints_toner_hp
from kostili import kostil_base_get_list_ip as list_ip

# Временный костыль ip_list - список Ip адрессов




def get_data_printer(ip_address):
    # логика на определение производителя принтера,
    url = f'http://{ip_address}'
    response = requests.get(url)
    if 'KYOCERA' in response.text:
        data = get_prints_toner_kyocera(ip_address)
        print(f'{ip_address}: Toner - {data[0]}, Prints - {data[1]}')

    elif 'HP LaserJet' in response.text:
        data = get_prints_toner_hp(ip_address)
        print(f'{ip_address}: Toner - {data[0]}, Prints - {data[1]}')
    else:
        print(ip_address, 'Неверный ip')

def getting_info():
    for ip_address in list_ip():
        try:
            info = get_data_printer(ip_address)
        except (ValueError, IndexError, requests.exceptions.ConnectTimeout):
            print(f'{ip_address}- fail get')







getting_info()