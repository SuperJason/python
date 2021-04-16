#!/usr/bin/env python3

# TCP SERVER
import socket
import threading

def tcplink(sock,addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('welcome!'.encode('utf-8'))
    while True:
        data=sock.recv(1024)
        if data=='exit' or not data:
            break;
        sock.send(('hello %s'%data).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed' % addr)

s=socket.socket()
s.bind(('127.0.0.1',9999))
s.listen(5)
print('serve is waiting connect.....')

while True:
    sock,addr=s.accept()
    t=threading.Thread(target=tcplink,args=(sock,addr))
    t.start()
