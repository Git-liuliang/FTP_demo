from src import model_client as C


ftp = C.FTP_client('127.0.0.1',8888)
ftp.client_connect_auth()

while True:
    username = input("username>>").strip()
    passwd = input("passwd>>").strip()
    res = ftp.client_user_auth(username,passwd)
    if res == 'no':
        print('########用户名密码不正确，请重试######')
        continue

    while True:
        print('#######欢迎光临',username,'#######')
        print('dir：查看目录，cd：切换目录，upload：上传，download：下载')
        cmd = input("cmd>>").strip()
        ftp.cmd_send(cmd)

