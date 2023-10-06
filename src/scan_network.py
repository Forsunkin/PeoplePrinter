import socket
from scapy.all import ARP, Ether, srp


def scan_local_network():
    # Определение диапазона IP-адресов в локальной сети
    ip_range = "192.168.1.1/24"  # Замените на ваш диапазон IP-адресов

    # Создание Ethernet-кадра
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Отправка ARP-запросов в сеть и получение ответов
    result = srp(packet, timeout=3, verbose=0)[0]

    # Обработка полученных ответов
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None


# Вызов функции scan_local_network() для сканирования сети
devices = scan_local_network()

# Вывод результатов
for device in devices:
    print("IP адрес:", device['ip'])
    print("MAC адрес:", device['mac'])
    hostname = get_hostname(device['ip'])
    if hostname:
        print("Имя хоста:", hostname)
    else:
        print("Не удалось получить имя хоста")
    print()