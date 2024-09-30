'''
задаем параметр (ip,name)

скрипт ищет файл "compname.txt" на удаленном диске С через ftp.
если файла нет, то создает новый файл с именем txt указанный в параметре

если файл есть то ничего не делает

1. задаём адрес компа и его имя из списк  (адрес, имя)
2. соединяемся по ftp на компьютер и ищем диск С
3. считываем корень и ищем файл compname.txt
4. читаем имя компьютера
5. проверяем, совпадает ли пара имя компьютера,ip с сохраненным ранее списком
6.

'''
addr_names = (('192.168.0.145','user'),)

import ftplib
import os
'''
 class ftplib.FTP(host='', user='', passwd='', acct='', timeout=None, source_address=None, *, encoding='utf-8')¶
    Return a new instance of the FTP class.
    Parameters:
            host (str) – The hostname to connect to. If given, connect(host) is implicitly called by the constructor.
            user (str) – The username to log in with (default: 'anonymous'). If given, login(host, passwd, acct) is implicitly called by the constructor.
            passwd (str) – The password to use when logging in. If not given, and if passwd is the empty string or "-", a password will be automatically generated.
            acct (str) – Account information to be used for the ACCT FTP command. Few systems implement this. See RFC-959 for more details.
            timeout (float | None) – A timeout in seconds for blocking operations like connect() (default: the global default timeout setting).
            source_address (tuple | None) – A 2-tuple (host, port) for the socket to bind to as its source address before connecting.
            encoding (str) – The encoding for directories and filenames (default: 'utf-8').
'''
find_file_name = 'name.txt'
computer_name = 'user1'
remoute_comp_name = ''

print(addr_names[0][0])

con_ftp = ftplib.FTP(host=addr_names[0][0])
con_ftp.login( user='user', passwd='Q1werty')
con_ftp.cwd('c')
dir_c = con_ftp.nlst()

def get_file():
    with open('tmp_' + find_file_name, 'wb') as res_file:
        con_ftp.retrbinary(f'RETR {find_file_name}', res_file.write)
    return 0

def create_local_file():
    print('файл для отправки ненайден')
    with open(find_file_name, 'w') as create_file:
        create_file.write(computer_name)
    return 0

def send_file():
    with open(find_file_name, 'rb') as send_file:
        con_ftp.storbinary(f'STOR {find_file_name}', send_file)
    print(f'Send file {find_file_name}  Done')
    return 0

def check_local_file():
    try:
        with open('tmp_' + find_file_name, 'r') as tmp_file:
           global remoute_comp_name
           remoute_comp_name = tmp_file.readline()

    except:
        print('файл не найден')

    print(f'Имя удаленного компьютера : {remoute_comp_name}')



if find_file_name in dir_c:
    print(f'На сервере Ftp:{addr_names[0][0]} Нашли {find_file_name}')
    get_file()
    check_local_file()

else:
    create_local_file()
    send_file()

#
# print('recive Done')
con_ftp.quit()