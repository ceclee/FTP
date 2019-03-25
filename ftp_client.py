from socket import *
import sys
import os
import time

class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    def do_list(self):
        self.sockfd.send(b'l')
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '**':
                    break
                print(data)
            print('接受完毕!')
            return
        else:
            print('文件列表请求失败!!')
            return
    def do_get(self,filename):
        x = 'g'+' '+filename
        self.sockfd.send(x.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            fd = open(filename,'w')
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '**':
                    break
                fd.write(data)
            fd.close()
            print('%s下载完成'%filename)
            return

        else:
            print('下载失败!')
            return

    def do_put(self,filename):
        try:
            fd = open(filename,'rb')
        except:
            print('上传的文件不存在')
            return

        self.sockfd.send(('p'+' '+filename).encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            print('可以接收｀｀')
            for line in fd:
                self.sockfd.send(line)
            fd.close()
            time.sleep(0.1)
            self.sockfd.send(b"**")
            print("success!")
            return
        else:
            print('上传文件失败')
            return

        self.sockfd.send(b'put')
    def do_quit(self):
        self.sockfd.send(b"q")


def main():
    if len(sys.argv)!=3:
        print("error")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024

    sockfd = socket()
    sockfd.connect(ADDR)
    ftp = FtpClient(sockfd)
    while True:
        print('*****命令选项*****')
        print('*****list*****')
        print('get')
        print('put')
        print('quit')
        data = input('shu ru:')

        if data == 'list':
            ftp.do_list()
        elif data[:3] == 'get':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[:3] == 'put':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)
        elif data == "quit":
            ftp.do_quit()
            sockfd.close()
            os._exit(0)
        else:
            print('input again:')
            continue





if __name__ == "__main__":
    main()

