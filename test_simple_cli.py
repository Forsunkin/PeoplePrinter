zdarova = 'Добро пожаловать, получть список команд: -help'
print(zdarova)

while True:
    x = input('>')
    if x == '-help':
        print('''Список команд:
        -get_ip (получтиь все ip принтеров)
        -exit (завершить работу)''')
    elif x == '-get_ip':
        print('zapros v bazu')
    elif x == '-exit':
        print('adios')
        break
    else:
        print('неверная команда, -help для помощи')

