from socket import *
import os
import sys
import signal,time


class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd
    def do_list(self):
        filelist = os.listdir('./')
        self.connfd.send(b'OK')
        time.sleep(0.1)
        for file in filelist:
            if file[0] != '.' and os.path.isfile('./'+file):
                self.connfd.send(file.encode())
                time.sleep(0.1)
        self.connfd.send(b'**')
        print('文件列表发送完毕')
        return
    def do_get(self,filename):
        try:
            fd = open(filename,'rb')
        except:
            self.connfd.send(b'fail')
        self.connfd.send(b'ok')
        time.sleep(0.1)
        for line in fd:
            self.connfd.send(line)
        fd.close()
        time.sleep(0.1)
        self.connfd.send(b'**')
        print("文件发送成功")
        return
    def do_put(self,filename):
        try:
            fd = open(filename,'w')
        except:
            self.connfd.send(b'failed')
        self.connfd.send(b'ok')
        while True:
            data = self.connfd.recv(1024).decode()
            if data == '**':
                break
            fd.write(data)
        fd.close()
        print('接收完毕')



def main():
    if len(sys.argv)!=3:
        print("error")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024

    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(5)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit(0)
        except Exception:
            continue
        print("connect:",addr)
        pid = os.fork()
        if pid < 0:
            print("fail for recreation")
            continue
        elif pid == 0:
            sockfd.close()
            ftp = FtpServer(connfd)
            while True:
                data = connfd.recv(BUFFERSIZE).decode()
                if data[0] == "l":
                    ftp.do_list()
                elif data[0] == "g":
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == "p":
                    filename = data.split(' ')[-1]
                    ftp.do_put(filename)
                elif data == "q":
                    print("客户端退出!")
                    sys.exit()
        else:
            connfd.close()
            continue



if __name__ == "__main__":
    main()