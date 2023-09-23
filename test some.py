from src.manufacturers.KYOCERA.kyocera_3040 import Kyocera3040
#
# ip = '192.168.1.36'
# printer = PeoplePrinter(ip)
# print(printer.full_info())


ip = '192.168.1.33'
printer = Kyocera3040(ip)
print(printer.full_info())