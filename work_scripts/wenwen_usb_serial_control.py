#!/usr/bin/env python3
"""
    This scripts is created to control orion boot up to factory mode and control factory test.

    $ sudo pip3 install pyserial
    $ sudo pip3 install pyudev

    output example:
     ---------- pyudev version: 0.21.0 ---------- 
     ----------   udev version: 204    ---------- 
     --------------------
    Please input AT command: 
    --------------------
      idVendor: 0e8d
      idProduct: 2000
      product: MT65xx Preloader
            cmd: 'FACTFACT' (10 bytes sended)

    --------------------
      idVendor: 0e8d
      idProduct: 2006
      product: mt6763
            cmd: 'AT+START' (10 bytes sended)
    6 byts received: b'pass\r\n'
            cmd: 'AT+VERSION' (12 bytes sended)
    6 byts received: b'pass\r\n'
    --------------------
    Please input AT command: AT+HWID       
            cmd: 'AT+HWID' (9 bytes sended)
    3 byts received: b'S0\n'
    --------------------
    Please input AT command: AT+READWIFIMAC
            cmd: 'AT+READWIFIMAC' (16 bytes sended)
    17 byts received: b'20:000000000000\r\n'
    --------------------
    Please input AT command: quit

"""

import sys
import os
import serial
import pyudev
import time

class USBDetect():
    def __init__(self, PreCB=None, ATCB=None):
        self.pid = ''
        self.vid = ''
        self.product = ''
        self.com_online = False
        self.pre_cb = PreCB
        self.at_cb = ATCB

        print(' ---------- pyudev version: ' + str(pyudev.__version__) + ' ---------- ')
        print(' ----------   udev version: '+ str(pyudev.udev_version()) + '    ---------- ')
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        self.observer = pyudev.MonitorObserver(monitor, self.event_cb)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def event_cb(self, action, device):
        if action == 'add':
            #print('device: ' + str(device))
            #print('device.sys_name: ' + str(device.sys_name))
            if str(device.subsystem) == 'usb' and str(device.device_type) == 'usb_device':
                node = device.sys_path + '/idVendor'
                print('\n--------------------')
                if os.path.exists(node):
                    with open(node, 'r') as f:
                        value = f.read()
                        print('  idVendor: ' + value[:-1])
                        self.vid = value[:-1]
                else:
                    print(node + ' dosen\'t exists!')

                node = device.sys_path + '/idProduct'
                if os.path.exists(node):
                    with open(node, 'r') as f:
                        value = f.read()
                        print('  idProduct: ' + value[:-1])
                        self.pid = value[:-1]
                else:
                    print(node + ' dosen\'t exists!')

                node = device.sys_path + '/product'
                if os.path.exists(node):
                    with open(node, 'r') as f:
                        value = f.read()
                        print('  product: ' + value[:-1])
                        self.product = value[:-1]
                else:
                    print(node + ' dosen\'t exists!')

            if str(device.sys_name) == 'ttyACM0':
                if self.product == 'mt6763' and self.pid == '2006' and self.vid == '0e8d':
                    self.com_online = True
                    if self.at_cb:
                        self.at_cb()

                if self.product == 'MT65xx Preloader' and self.pid == '2000' and self.vid == '0e8d':
                    if self.pre_cb:
                        self.pre_cb()

class ATPort():
    def __init__(self, port_name):
        if port_name == None:
            return
        self.port = serial.Serial(port=port_name, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=2)

    def ATSend(self, cmd):
        send_cmd = (cmd + '\r\n').encode(encoding='utf-8')
        cnt = self.port.write(send_cmd)
        self.port.flush()
        print('\tcmd: \'%s\' (%d bytes sended)'%(cmd, cnt))
        return cnt

    def ATReceive(self):
        resp = self.port.readline()
        if len(resp) > 0:
            print('%d byts received: %s'%(len(resp), resp))

    def Close(self):
        self.port.close()

def PreLoaderAT():
    global com_dev_name 

    port = ATPort(com_dev_name)
    Cmd = 'FACTFACT'
    port.ATSend(Cmd)
    time.sleep(0.3)
    port.Close()

def FactoryAT():
    global com_dev_name 

    port = ATPort(com_dev_name)
    Cmd = 'AT+START'
    port.ATSend(Cmd)
    port.ATReceive()

    time.sleep(0.3)

    Cmd = 'AT+VERSION'
    port.ATSend(Cmd)
    port.ATReceive()

    time.sleep(0.3)
    port.Close()
    print('--------------------\nPlease input AT command: ', end='')

if __name__ == '__main__':
    global com_dev_name 
    if len(sys.argv) > 1:
        com_dev_name = sys.argv[1]
    else:
        com_dev_name ='/dev/ttyACM0'

    usb_detect = USBDetect(PreCB=PreLoaderAT, ATCB=FactoryAT)
    usb_detect.start()

    while (True):
        Cmd = input('--------------------\nPlease input AT command: ')
        if Cmd == 'quit':
            break
        elif Cmd == 'boot':
            port = ATPort(com_dev_name)
            Cmd = 'AT+START'
            port.ATSend(Cmd)
            port.ATReceive()

            time.sleep(0.3)

            Cmd = 'AT+VERSION'
            port.ATSend(Cmd)
            port.ATReceive()

            time.sleep(0.3)
            port.Close()
        else:
            port = ATPort(com_dev_name)
            port.ATSend(Cmd)
            port.ATReceive()
            port.Close()

