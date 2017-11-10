import os
from lib.comm import *
class Auth:

    @classmethod
    def server_connect_auth(self,connector):
        print('开始验证新链接的合法性')
        msg = os.urandom(32)
        connector.send(msg)
        auth_msg = Md5_salt.msg_md5(msg)
        data = connector.recv(32).decode('utf-8')
        print('auth_msg:',auth_msg)
        print('data',data)
        if auth_msg == data:
            connector.send('ok'.encode('utf-8'))
            print('链接验证合法！')
            return 'ok'
        else:

            connector.send('no'.encode('utf-8'))
            print('链接验证不合法！')
            return 'no'

    @classmethod
    def client_connect_auth(self,client):
        data = client.recv(32)
        msg = Md5_salt.msg_md5(data)
        client.send(msg.encode('utf-8'))
        msg_info = client.recv(2)
        if msg_info.decode('utf-8') == 'ok':
            print('ok')
        else:
            print('no')

    @classmethod
    def server_user_auth(self,connector):

                msg0 = connector.recv(4)
                header_len = struct.unpack('i', msg0)[0]
                msg1 = connector.recv(header_len)
                # total_size = json.loads(msg1.decode('utf-8'))['total_size']
                username = json.loads(msg1.decode('utf-8'))['username']
                passwd = json.loads(msg1.decode('utf-8'))['passwd']
                ps = Config_hander.getuserinfo(username,'passwd')
                if ps == passwd:
                    print('登陆成功！')
                    return username
                else:
                    print('登录失败')
                    exit()



    @classmethod
    def client_user_auth(self,client):
        username = input("username>>").strip()
        passwd = input("passwd>>").strip()
        msg = username + passwd
        header = Make_header.auth_header(len(msg), username, passwd)
        client.send(header[0])
        client.send(header[1])

