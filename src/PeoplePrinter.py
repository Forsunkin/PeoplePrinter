from src.InitPrinter import InitPrinter

class PeoplePrinter():

    def __init__(self, ip_address):
        info = InitPrinter(ip_address).init_info






if __name__ == "__main__":
    ip = '192.168.1.36'

    print(PeoplePrinter(ip).info)
