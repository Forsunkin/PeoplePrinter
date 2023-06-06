import requests
url = 'http://192.168.1.38/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'



def get_data(url):
    r = requests.get(url)
    print(r.text)


get_data(url)