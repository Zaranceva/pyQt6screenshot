import ftplib
import os
import json


class ConnrectToFtp(ftplib.FTP):
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
    FILENAME = 'name.txt'

    def __init__(self, host = '0.0.0.0', compname = ''):
        # соединяемся с сервером и  сохраняем список директории диска С

        ftplib.FTP.__init__(self, host=host, user='user', passwd='Q1werty', timeout= 2)
        self.dir_list = []
        self.cwd('c')
        self.dir_list = self.nlst()
        self.current_ip = host
        self.local_name = compname
        self.remote_name = ''


    def find_comp_name(self,filename= FILENAME):
        # Ищем в директории файл filename  открываем и сверяем имя компьютера.
        # Возвращаем найденое имя или пустую строку
        if filename in self.dir_list:
            print("имя найдено, открываем и возвращаем имя компьютера")
            with open(f'tmp_{filename}', 'bw') as tmp_file:
                self.retrbinary(f'RETR {filename}', tmp_file.write)
            with open(f'tmp_{filename}', 'r') as tmp_file:
                self.remote_name = tmp_file.readline()
        else:
            print('файл не найден')
            self.remote_name = ''

        return self.remote_name

    def create_and_send_temp_file(self, filename= FILENAME):
        # создает временный файл с правильными данными по имени компьютера
        with open(f'send_tmp_{filename}','w') as tmp_file:
            tmp_file.write(f'{self.local_name}')
        with open(f'send_tmp_{filename}','rb') as tmp_file:
            self.storbinary(f'STOR {filename}', tmp_file)
        print(f'файл {filename} с именем компьютера {self.local_name} отправлен на {self.current_ip}')

    def del_remoute_file(self):
        self.delete(self.FILENAME)

if __name__ == '__main__':

    # если нужно перезаписать имя компа на удаленном хосте, то ставим True.
    del_all_wrong_ips = False

    with open('ip_name.json','r') as ip_name:
        list_names_ip = json.load(ip_name)

    print(list_names_ip)

    for key, item in list_names_ip.items() :
        try:
            ftp_conn = ConnrectToFtp(compname=key, host=item)
            remout_comp_name = ftp_conn.find_comp_name()
            if remout_comp_name == key:
                print(remout_comp_name, item)
            else:
                if remout_comp_name == '':
                    ftp_conn.create_and_send_temp_file()
                else:
                    print(remout_comp_name, key, item)
                    if del_all_wrong_ips: ftp_conn.del_remoute_file()


            ftp_conn.close()
        except:
            print(f'Соединение с {item} говно!')

