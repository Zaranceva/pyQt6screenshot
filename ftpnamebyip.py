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
addr_names = (("192.168.0.145",'user'))

import ftplib

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

con_ftp = ftplib.FTP(host='192.168.0.145')
con_ftp.login( user='user', passwd='Q1werty')
dir_c = [con_ftp.dir('c')]
#print(dir_c)
for line in dir_c:
    print(line)

with open('main.py', 'rb') as send_file:
    con_ftp.storbinary('STOR main.py', send_file)

print('Send Done')

with open('main2.py', 'wb') as res_file:
    con_ftp.retrbinary('RETR main.py', res_file.write)

print('recive Done')
con_ftp.quit()