#!/usr/bin/env python3

# TCP CLINET
import socket
import threading

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in ['zhangkang','jack','tom']:
    s.sendto(i.encode('utf-8'), ('127.0.0.1', 9999))
    data=s.recv(1024)
    print(data)
s.close()
