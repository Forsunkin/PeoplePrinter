from src.InitPrinter import InitPrinter


class PeoplePrinter:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    @property
    def init_printer(self):
        init_info = InitPrinter(self.ip_address).init_info
        return init_info



if __name__ == "__main__":
    ip = '192.168.1.36'
    print(PeoplePrinter(ip).init_printer)
