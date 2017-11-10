import os
import time
import sys
import hashlib,hmac,json,struct
import configparser
from conf import settings

class Config_hander:

    @classmethod
    def getConfig(self,section,key):
        config = configparser.ConfigParser()
        path = settings.MARGS_DIR
        config.read(path)
        return config.get(section,key)
    @classmethod
    def modConfig(self,section,key,value):
        config = configparser.ConfigParser()
        path = settings.MARGS_DIR
        config.read(path)
        config.set(section,key,value)
        config.write(open(path, "w"))

    @classmethod
    def getuserinfo(self, section, key):
        config = configparser.ConfigParser()
        path = settings.USERINFO
        config.read(path)
        return config.get(section, key)




# aa = Config_hander.getConfig('processbar','width')
# print(aa)
# bb = Config_hander.modConfig('processbar','width','100')



class Processbar:
    '''###进度条########'''
    width = int(Config_hander.getConfig('processbar','width'))
    @classmethod
    def process(self,percent):
        if percent >=1:
            percent = 1
        showpro = '[%%-%ds]'%self.width% (int(self.width*percent)*'#')
        print('\r%s %d%%'%(showpro,int(percent*100)),file=sys.stdout,flush=True,end='')


class Md5_salt:
    '''md5 加盐'''
    secret_key = Config_hander.getConfig('md5_salt','secretkey')
    @classmethod
    def file_md5(self,file):
        m=hmac.new(self.secret_key.encode('utf-8'))

        with open(file,'rb') as f:
            for line in f:
                #print(line)
                m.update(line)
        return m.hexdigest()

    @classmethod
    def msg_md5(self,msg):
        m = hmac.new(self.secret_key.encode('utf-8'))
        m.update(msg)
        return m.hexdigest()

# aa = Md5_salt.file_md5('E:/pycharn/socket_train/FTP_demo/src/model_client.py')
# print(aa)
# bb = Md5_salt.msg_md5('aaaaaa')
# print(bb)

class Make_header:
    @classmethod
    def makeheader(self,fsize,filename,md5):
        dic_head = {'total_size': fsize, 'file_name': filename, 'md5': md5}
        rr = json.dumps(dic_head)

        head_bytes = bytes(rr.encode('utf-8'))

        msg0 = struct.pack('i', len(head_bytes))
        msg1 = head_bytes
        msg_list = [msg0, msg1]
        return msg_list

    @classmethod
    def auth_header(self, fsize, username,passwd):
        dic_head = {'total_size': fsize, 'username': username,'passwd':passwd}
        rr = json.dumps(dic_head)

        head_bytes = bytes(rr.encode('utf-8'))

        msg0 = struct.pack('i', len(head_bytes))
        msg1 = head_bytes
        msg_list = [msg0, msg1]
        return msg_list

    @classmethod
    def msgheader(self, fsize):
        dic_head = {'total_size': fsize}
        rr = json.dumps(dic_head)

        head_bytes = bytes(rr.encode('utf-8'))

        msg0 = struct.pack('i', len(head_bytes))
        msg1 = head_bytes
        msg_list = [msg0, msg1]
        return msg_list


