#!/usr/bin/python

from socket import *
import struct
import socket
import json
from lib.auth import Auth

class FTP_server:
    def __init__(self,bind_ip,bind_port,max_wait):
        self.ftpserver = socket.socket()
        self.ftpserver.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.ftpserver.bind((bind_ip,bind_port))
        self.ftpserver.listen(max_wait)


    def get_request(self):
        return self.ftpserver.accept()

    def close_request(self,request):
        request.close()

    def close(self):
        self.ftpserver.close()


    def msg_recv(self):

        while True:
            self.conn, self.re_addr = self.get_request()
            msg0 = self.conn.recv(4)
            header_len = struct.unpack('i',msg0)[0]
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

        self.close()

    def run(self):
        # print("starting........")
        self.conn, self.re_addr = self.get_request()
        Auth.server_connect_auth(self.conn)
        print("starting........")
        while True:
            re_l = self.conn.recv(4)
            re_len = struct.unpack('i', re_l)[0]
            dd = self.conn.recv(re_len)
            ss = json.loads(dd.decode('utf-8'))['total_size']
            filename = json.loads(dd.decode('utf-8'))['file_name']
            rec_data = 0
            total = b''
            print(ss)
            if ss > 0:
                while rec_data < ss:
                    data = self.conn.recv(4)
                    total = total + data
                    rec_data += len(data)

                with open(filename, 'wb') as w:
                    w.write(total)

        self.close_request(self.conn)

        self.close()

ftp = FTP_server('127.0.0.1',8888,5)
# ftp.msg_recv()
ftp.run()

