from src import model_client as C
from conf import settings
from lib import comm

def main():

    ip = comm.Config_hander.getConfig('client','ip')
    port = comm.Config_hander.getConfig('client', 'port')
    ftp = C.FTP_client(ip,int(port))
    ftp.client_connect_auth()

    while True:
        username = input("username>>").strip()
        passwd = input("passwd>>").strip()
        res = ftp.client_user_auth(username,passwd)
        if res == 'no':
            print('########用户名密码不正确，请重试######')
            continue

        while True:

            print('\n#######欢迎光临',username,'#######')
            print('dir：查看目录，cd：切换目录，upload：上传，download：下载')
            cmd = input("cmd>>").strip()
            ftp.cmd_send(cmd)

