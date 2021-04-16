#!/usr/bin/env python3

# UDP SERVER
import socket
import threading

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',9999))
print('udp serve is waiting connect.....')

while True:
    data, addr=s.recvfrom(1024)
    print('Received from %s:%s'%addr)
    s.sendto(('Hello, %s'%data).encode('utf-8'), addr)
