from src import model_server as S
from lib import comm

def main():
    print("等待连接....")
    ip = comm.Config_hander.getConfig('server', 'ip')
    port = comm.Config_hander.getConfig('server', 'port')
    listen = comm.Config_hander.getConfig('server', 'listen')
    ftp = S.FTP_server(ip,int(port),int(listen))

    print('来自',ftp.re_addr)
    ftp.server_connect_auth()
    while True:

        info = ftp.server_user_auth()
        if info == 300:
            continue
        else:
            ftp.cmd_recv(info)


