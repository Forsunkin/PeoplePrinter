from src.InitPrinter import InitPrinter
from src.manufacturers.KYOCERA.major_kyocera import KyoceraMajor


class PeoplePrinter(InitPrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)






if __name__ == "__main__":
    ip = '192.168.1.36'
    printer = PeoplePrinter(ip)
    print(printer.select_by_prod())