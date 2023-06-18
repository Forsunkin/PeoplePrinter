import requests
from bs4 import BeautifulSoup
import re

url = "http://192.168.1.99/info_suppliesStatus.html?tab=Home&menu=SupplyStatus" # SPA

def get_data(url):
    source_code = requests.get(url).text
    bs_code = BeautifulSoup(source_code, "html.parser")
    data_numbers = bs_code.find_all(class_='itemSpsFont')
    data_toner = bs_code.find(class_='SupplyName width35 alignRight')

    
    toner_lvl = re.findall(r"(\d+)", data_toner.text)
    return result

print(get_data(url))
