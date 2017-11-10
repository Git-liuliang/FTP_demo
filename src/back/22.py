#!/usr/bin/python
import json
import os
import socket
import struct
import time

from lib.auth import Auth
from lib.comm import Processbar as p
from lib.comm import Make_header


class FTP_client:
    def __init__(self,ip,ip_port):
        self.ftpclient = socket.socket()
        self.ftpclient.connect((ip,ip_port))
        # self.ip = ip
        # self.ip_port = ip_port

    def makeheader(self,fsize,filename):
        dic_head = {'total_size': fsize, 'file_name': filename, 'MD5': 123456}
        rr = json.dumps(dic_head)

        head_bytes = bytes(rr.encode('utf-8'))

        msg0 = struct.pack('i', len(head_bytes))
        msg1 = head_bytes
        msg_list = [msg0, msg1]
        return msg_list

    def msg_send(self):
        while True:
            username = input("username>>").strip()
            passwd = input("passwd>>").strip()
            msg = username+passwd
            header = Make_header.auth_header(len(msg),username,passwd)
            self.ftpclient.send(header[0])
            self.ftpclient.send(header[1])
            # self.ftpclient.send(msg.encode('utf-8'))
            # self.ftpclient.close()

    def msg_recv(self):

        msg0 = self.ftpclient.recv(4)
        header_len = struct.unpack('i', msg0)[0]
        msg1 = self.ftpclient.recv(header_len)
        total_size = json.loads(msg1.decode('utf-8'))['total_size']
        rec_data = 0
        total = b''
        if total_size > 0:
            while rec_data < total_size:
                data = self.ftpclient.recv(4)
                total = total + data
                rec_data += len(data)
            print(total.decode('utf-8'))



    def run(self):
        Auth.client_connect_auth(self.ftpclient)
        Auth.client_user_auth(self.ftpclient)
        while True:
            msg = input('>>>:').strip()
            filepath = (msg.encode('utf-8'))
            fsize = os.path.getsize(filepath)
            print(fsize)
            filename = os.path.split(msg)[1]

            header = self.makeheader(fsize, filename)

            self.ftpclient.send(header[0])
            self.ftpclient.send(header[1])
            with open(msg, 'rb') as f:
                rec_size = 0
                for line in f:
                    self.ftpclient.send(line)
                    time.sleep(0.3)
                    rec_size +=len(line)
                    percent = rec_size/fsize
                    p.process(percent)
        self.ftpclient.close()




ftp = FTP_client('127.0.0.1',8888)

    # ftp.msg_send()

ftp.run()
# ftp.msg_send('egon')
#
# ftp = FTP_client('127.0.0.1',8888)
# while True:
#     ftp.msg_send('egon')
#     ftp.msg_send('xinwei')
# self.ftpclient.close()
