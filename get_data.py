import requests
from bs4 import BeautifulSoup
import re

url = "http://192.168.1.99/info_suppliesStatus.html?tab=Home&menu=SupplyStatus" # ОБ

def get_data(url):
    source_code = requests.get(url).text
    bs_code = BeautifulSoup(source_code, "html.parser")
    data = bs_code.findAll(class_='itemSpsFont')
    print(data)


get_data(url)
