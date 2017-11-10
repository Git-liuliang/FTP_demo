#!/usr/bin/python
import json
import os
import socket
import struct
import time

from lib.auth import Auth
from lib.comm import Processbar as p, Md5_salt, Config_hander, Timer
from lib.comm import Make_header

timeout = 10
socket.setdefaulttimeout(timeout)

class FTP_client:
    def __init__(self,ip,ip_port):
        self.ftpclient = socket.socket()
        self.ftpclient.connect((ip,ip_port))


    # def msg_send(self):
    #     # while True:
    #         username = input("username>>").strip()
    #         passwd = input("passwd>>").strip()
    #         msg = username+passwd
    #         header = Make_header.auth_header(len(msg),username,passwd)
    #         self.ftpclient.send(header[0])
    #         self.ftpclient.send(header[1])


    def msg_recv(self):

        msg0 = self.ftpclient.recv(4)
        header_len = struct.unpack('i', msg0)[0]
        msg1 = self.ftpclient.recv(header_len)
        total_size = json.loads(msg1.decode('utf-8'))['total_size']
        rec_data = 0
        total = b''
        if total_size > 0:
            while rec_data < total_size:
                data = self.ftpclient.recv(1024)
                total = total + data
                rec_data += len(data)
            print(total.decode('gbk'))

    def cmd_send(self,cmd):

            if cmd == 'upload':
                self.ftpclient.send(cmd.encode('utf-8'))
                self.run()
            elif cmd == 'download':
                self.ftpclient.send(cmd.encode('utf-8'))
                self.dowload()

            else:
                self.ftpclient.send(cmd.encode('utf-8'))
                self.msg_recv()


    def dowload(self):
        msg = input('输入下载的文件名>>>:').strip()
        self.ftpclient.send(msg.encode('utf-8'))

        re_l = self.ftpclient.recv(4)
        re_len = struct.unpack('i', re_l)[0]
        dd = self.ftpclient.recv(re_len)
        ss = json.loads(dd.decode('utf-8'))['total_size']
        filename = json.loads(dd.decode('utf-8'))['file_name']
        rec_data = 0
        total = b''
        print('ss', ss)
        if ss > 0:
            while rec_data < ss:
                data = self.ftpclient.recv(4)
                total = total + data
                rec_data += len(data)
                percent = rec_data / ss
                p.process(percent)
            dir = Config_hander.getConfig('download_dir','dir')
            path = os.path.join(dir, filename)
            with open(path, 'wb') as w:
                w.write(total)
            print("download done")




    def run(self):

            msg = input('输入上传路径>>>:').strip()
            filepath = (msg.encode('utf-8'))
            fsize = os.path.getsize(filepath)
            print(fsize)
            filename = os.path.split(msg)[1]
            md5 = Md5_salt.file_md5(msg)
            header = Make_header.makeheader(fsize, filename,md5)

            self.ftpclient.send(header[0])
            self.ftpclient.send(header[1])

            try:
                Timer.circle(10)
                last_data = self.ftpclient.recv(1024).decode('utf-8')
                print('last data ',last_data)
                with open(msg, 'rb') as f:
                    rec_size = 0
                    for line in f:
                        rec_size += len(line)
                        if rec_size >= int(last_data):
                            self.ftpclient.send(line)
                        # time.sleep(0.3)
                        # rec_size += len(line)
                            percent = rec_size / fsize
                            p.process(percent)


            except Exception:
                print('new file')


                with open(msg, 'rb') as f:
                    rec_size = 0
                    for line in f:
                        self.ftpclient.send(line)
                        # time.sleep(0.3)
                        rec_size +=len(line)
                        percent = rec_size/fsize
                        p.process(percent)




    def client_connect_auth(self):
        '''验证客户端连接合法性，防止非法连接'''
        data = self.ftpclient.recv(32)
        msg = Md5_salt.msg_md5(data)
        self.ftpclient.send(msg.encode('utf-8'))
        msg_info = self.ftpclient.recv(2)
        if msg_info.decode('utf-8') == 'ok':
            print('验证链接ok')
        else:
            print('no')

    def client_user_auth(self,username,passwd):
        '''用户登录验证'''
        # username = input("username>>").strip()
        # passwd = input("passwd>>").strip()
        msg = username + passwd
        header = Make_header.auth_header(len(msg), username, passwd)
        self.ftpclient.send(header[0])
        self.ftpclient.send(header[1])
        result = self.ftpclient.recv(1024)
        return result.decode('utf-8')