from src.InitPrinter import InitPrinter
from src.manufacturers.KYOCERA.major_kyocera import KyoceraMajor
from src.manufacturers.HP.major_hp import HPMajor
from src.manufacturers.PANTUM.major_pantum import PantumMajor
from src.manufacturers.Xerox.major_xerox import XeroxMajor

class PeoplePrinter(InitPrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)

    def full_info(self):
        if self.prod == 'KYOCERA':
            x = KyoceraMajor
        elif self.prod == 'HP':
            x = HPMajor
        elif self.prod == 'PANTUM':
            x = PantumMajor
        elif self.prod == 'XEROX':
            x = XeroxMajor
        else:
            return 'Производитель неизвестен'
        return self.work(x(self.ip_address))

    def work(self, printer):
        return {
                'ip_address': self.ip_address,
                'mac_address': printer.mac,
                'host_name': printer.host_name,
                'prod': self.prod,
                'model': printer.model,
                'locate': self.locate,
                'toner_lvl': printer.toner,
                'prints_count': printer.prints_count,
                'status': 'Done'
                }


if __name__ == "__main__":
    ip = '192.168.2.184'
    printer = PeoplePrinter(ip)
    print(printer.full_info())