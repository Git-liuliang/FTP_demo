#!/usr/bin/python
from conf import settings
import subprocess
from socket import *
import struct
import socket
import json
from lib.comm import Processbar as p, Md5_salt
from lib.auth import Auth
from lib.comm import *

class FTP_server:
    def __init__(self,bind_ip,bind_port,max_wait):
        self.ftpserver = socket.socket()
        self.ftpserver.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.ftpserver.bind((bind_ip,bind_port))
        self.ftpserver.listen(max_wait)
        self.conn, self.re_addr = self.get_request()


    def get_request(self):
        return self.ftpserver.accept()

    def close_request(self,request):
        request.close()

    def close(self):
        self.ftpserver.close()

    def hert(self):
        print('消息来自>>', self.re_addr)
        msg0 = self.conn.recv(4)
        header_len = struct.unpack('i', msg0)[0]
        msg1 = self.conn.recv(header_len)
        total_size = json.loads(msg1.decode('utf-8'))['total_size']
        rec_data = 0
        total = b''
        if total_size > 0:
            while rec_data < total_size:
                data = self.conn.recv(4)
                total = total + data
                rec_data += len(data)
            print(total.decode('utf-8'))
        self.close_request(self.conn)

    def msg_recv(self):
        self.conn, self.re_addr = self.get_request()
        print('消息来自>>', self.re_addr)
        while True:


            msg0 = self.conn.recv(4)
            header_len = struct.unpack('i', msg0)[0]
            msg1 = self.conn.recv(header_len)
            # total_size = json.loads(msg1.decode('utf-8'))['total_size']
            username = json.loads(msg1.decode('utf-8'))['username']
            passwd = json.loads(msg1.decode('utf-8'))['passwd']
            print(username)
            print(passwd)
            # rec_data = 0
            # total = b''
            # if total_size > 0:
            #     while rec_data < total_size:
            #         data = self.conn.recv(4)
            #         total = total + data
            #         rec_data += len(data)
            #     print(total.decode('utf-8'))
        self.close_request(self.conn)


        self.close()


    def cmd_recv(self,username):
        # self.conn, self.re_addr = self.get_request()
        current_dir =os.path.join(settings.DB_DIR,username)
        try:
            while True:
                cmd = self.conn.recv(1024)
                print(cmd)
                res = cmd.decode('utf-8')
                if res == 'dir':
                    all = ' '.join(['dir',current_dir])
                    result = subprocess.Popen(all, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # data = result.stdout.read()
                    res = ''
                    for line in result.stdout:
                        data = line.decode('gbk')
                        if not data.startswith(' '):
                            res+=data
                    self.msg_send(res.encode('utf-8'))

                if res.split(' ')[0] == 'mkdir':
                    print('aaaaaaaa')
                    path = os.path.join(current_dir,res.split(' ')[1])
                    all = ' '.join(['mkdir',path])
                    result = subprocess.Popen(all, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    data = '创建成功'.encode('gbk')
                    self.msg_send(data)
                if res.split(' ')[0] == 'cd':
                    path = os.path.join(current_dir, res.split(' ')[1])
                    all = ' '.join(['cd',path])
                    current_dir = path
                    result = subprocess.Popen(all, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    data = '切换目录成功'.encode('gbk')
                    self.msg_send(data)
                if res == 'upload':
                    self.run(current_dir)
                if res == 'download':
                    self.download(current_dir)



        except ConnectionResetError:
            print("来自%s,端口为:%s的链接关闭" % (self.re_addr[0], self.re_addr[1]))

        self.conn.close()



    def download(self,current_dir):
        # Auth.client_connect_auth(self.ftpclient)
        # Auth.client_user_auth(self.ftpclient)
        while True:
            msg = self.conn.recv(1024).decode('utf-8')

            filepath = os.path.join(current_dir,msg)
            print(filepath)
            fsize = os.path.getsize(filepath)
            print(fsize)
            # filename = os.path.split(msg)[1]
            # print(filename.)
            header = Make_header.makeheader(fsize, msg)

            self.conn.send(header[0])
            self.conn.send(header[1])
            with open(filepath, 'rb') as f:
                rec_size = 0
                for line in f:
                    self.conn.send(line)
                    time.sleep(0.3)
                    rec_size +=len(line)
                    percent = rec_size/fsize
                    p.process(percent)






    def msg_send(self,msg):
            header = Make_header.msgheader(len(msg))
            self.conn.send(header[0])
            self.conn.send(header[1])
            self.conn.send(msg)
            # self.conn.close()

    def run(self,current_dir):
        # print("starting........")
        # self.conn, self.re_addr = self.get_request()
        # Auth.server_connect_auth(self.conn)
        # Auth.server_user_auth(self.conn)
        print("starting........")
        #####################

        ######################
        # while True:
        re_l = self.conn.recv(4)
        re_len = struct.unpack('i', re_l)[0]
        dd = self.conn.recv(re_len)
        ss = json.loads(dd.decode('utf-8'))['total_size']
        filename = json.loads(dd.decode('utf-8'))['file_name']
        md5 = json.loads(dd.decode('utf-8'))['md5']
        rec_data = 0
        total = b''
        print('ss', ss)
        if ss > 0:
            # while rec_data < ss:
            #     data = self.conn.recv(102)
            #     total = total + data
            #     rec_data += len(data)
            #
            # path = os.path.join(current_dir, filename)
            # with open(path, 'wb') as w:
            #     w.write(total)
            # print("upload done")
            while rec_data < ss:
                data = self.conn.recv(102)
                total = total + data
                rec_data += len(data)

                path = os.path.join(current_dir, filename)
                with open(path, 'ab') as w:
                    w.write(data)
            print("upload done")


    def server_connect_auth(self):
        '''验证客户端连接合法性，防止非法连接'''
        # self.conn, self.re_addr = self.get_request()
        print('开始验证新链接的合法性')
        msg = os.urandom(32)
        self.conn.send(msg)
        auth_msg = Md5_salt.msg_md5(msg)
        data = self.conn.recv(32).decode('utf-8')
        print('auth_msg:',auth_msg)
        print('data',data)
        if auth_msg == data:
            self.conn.send('ok'.encode('utf-8'))
            print('链接验证合法！')
            return 'ok'
        else:

            self.conn.send('no'.encode('utf-8'))
            print('链接验证不合法！')
            return 'no'



    def server_user_auth(self):
        '''用户登录认证'''
        # self.conn, self.re_addr = self.get_request()
        msg0 = self.conn.recv(4)
        header_len = struct.unpack('i', msg0)[0]
        msg1 = self.conn.recv(header_len)
        # total_size = json.loads(msg1.decode('utf-8'))['total_size']
        username = json.loads(msg1.decode('utf-8'))['username']
        passwd = json.loads(msg1.decode('utf-8'))['passwd']
        ps = Config_hander.getuserinfo(username, 'passwd')
        if ps == passwd:
            self.conn.send('ok'.encode('utf-8'))
            print('登陆成功！')
            return username
        else:
            print('登录失败')
            self.conn.send('no'.encode('utf-8'))
            return 300