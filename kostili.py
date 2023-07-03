
def kostil_base_get_list_ip():
    ip_list = []
    with open('ip_printers.txt') as f:
            file_list = f.read().splitlines()
            for ip in file_list:
                ip_list.append(ip)
    return ip_list



if __name__ == "__main__":
    print(kostil_base_get_list_ip())
