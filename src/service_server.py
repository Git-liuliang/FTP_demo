from src import model_server as S



ftp = S.FTP_server('127.0.0.1',8888,5)
ftp.server_connect_auth()
while True:

    info = ftp.server_user_auth()
    if info == 300:
        continue
    else:
        ftp.cmd_recv(info)

# ftp.cmd_recv()
