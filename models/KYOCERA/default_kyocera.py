import re
import requests


def get_prints_toner_kyocera(ip_address):
    url_counter = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    url_toner = f'http://{ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'

    headers_counter = {'Cookie': 'rtl=0; css=0',
                       'Referer': f'http://{ip_address}/startwlm/Hme_Paper.htm'}

    headers_toner = {'Cookie': 'rtl=0; css=0',
                     'Referer': f"http://{ip_address}/startwlm/Hme_Toner.htm"}

    page_code_config = requests.get(url_counter, headers=headers_counter)
    page_code_toner = requests.get(url_toner, headers=headers_toner)

    # Получение данных ко-ва оттисков
    printed_total = re.findall(r".*printertotal = \('(\d*)'\)", page_code_config.text)     # получить отпечатанные листы
    copy_total = re.findall(r".*copytotal = \('(\d*)'\)", page_code_config.text)           # получить сканы
    prints_count = int(printed_total[0]) + int(copy_total[0])                              # получить cумму

    # получение уровня тонера
    data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", page_code_toner.text)           # получить остаток тонера
    toner_lvl = int(data_toner[0])

    return toner_lvl, prints_count


if __name__ == "__main__":
    pass

