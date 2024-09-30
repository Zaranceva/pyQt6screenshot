import ftplib
import os

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
    def __init__(self, host = '0.0.0.0'):
        ftplib.FTP.__init__(self, host=host, user='user', passwd='Q1werty')
        self.dir_list = []
        self.cwd('c')
        self.dir_list = self.nlst()

    def find_comp_name(self,filename='name.txt', compname=''):
        # Ищем в директории файл filename  открываем и сверяем имя компьютера.
        # Возвращаем найденое имя или пустую строку
        if filename in self.dir_list:
            print("имя найдено, открываем и проверяем имя компьютера")
            with open(f'tmp_{filename}', 'bw') as tmp_file:
                self.retrbinary(f'RETR {filename}', tmp_file.write)
            with open(f'tmp_{filename}', 'r') as tmp_file:
                compname = tmp_file.readline()
        return compname


if __name__ == '__main__':

    lists_ip_names = (('192.168.0.145', 'user1'),('192.168.0.158', 'user2'),('192.168.0.31', 'terminal'))

    for item in lists_ip_names:

        ftp_conn = ConnrectToFtp(host=item[0])
        remout_comp_name = ftp_conn.find_comp_name(filename='name.txt')
        if remout_comp_name == item[1]:
            print(remout_comp_name, item[0])
        else:
            print(' ', item[0])
        ftp_conn.close()
