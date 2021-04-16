#!/usr/bin/env python3

# TCP CLINET
import socket
import threading

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('127.0.0.1',9999))
data=s.recv(1024)

print(data)
for i in ['zhangkang','jack','tom']:
    s.send(i.encode('utf-8'))
    data=s.recv(1024)
    print(data)
s.send('exit'.encode('utf-8'))
s.close()
