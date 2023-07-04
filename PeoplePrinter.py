import requests
import re
from kostili import kostil_base_get_list_ip as list_ip
from bs4 import BeautifulSoup
# класс на определение производителя, проверка корректности ip

class PPrinterConfig:
    def __init__(self, ip_address):
        self.ip











ip = '192.168.1.36'
printer = PeoplePrinter(ip)
printer.get_config()
print(printer.mac_address)





ip = '192.168.1.36'
# printer = PeoplePrinter(ip)
# printer.ip_address