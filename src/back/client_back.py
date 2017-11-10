#!/usr/bin/python
import json
import os
import socket
import struct
import time

from lib.auth import Auth
from lib.comm import Processbar as p


class FTP_client:
    def __init__(self,ip,ip_port):
        self.ftpclient = socket.socket()
        self.ftpclient.connect((ip,ip_port))

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
             msg = input(">>")
             header = self.makeheader(len(msg),0)
             self.ftpclient.send(header[0])
             self.ftpclient.send(header[1])
             self.ftpclient.send(msg.encode('utf-8'))
             self.ftpclient.close()



    def run(self):
        Auth.client_connect_auth(self.ftpclient)
        while True:
            msg = input('>>>:').strip()
            filepath = (msg)
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
