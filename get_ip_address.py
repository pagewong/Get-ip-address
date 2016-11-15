#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' get ip Address '

__author__ = 'Page Wong'

import array
import struct
import socket
import fcntl
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

'''
#获取IP地址功能 
'''
def get_ip_address():
    """
    先获取所有网络接口
    """
    
    SIOCGIFCONF = 0x8912
    SIOCGIFADDR = 0x8915
    BYTES = 4096         
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B',b'\0' * BYTES)
    bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]
    namestr = names.tostring()
    ifaces = [namestr[i:i+32].split('\0', 1)[0] for i in range(0, bytelen, 32)]
    
    '''
    再获取每个接口的IP地址
    '''
    iplist = []
    for ifname in ifaces:
        ip = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),SIOCGIFADDR,struct.pack('256s',ifname[:15]))[20:24])
        iplist.append(ifname+':'+ip)
    return iplist

    
'''
#把IP地址存入文件 
'''
def ip_save_file(iptxt):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('ipaddress.txt','w') as f:
        f.write(now+'\r\n')
        for ip in get_ip_address(): 
            f.write(ip+'\r\n')

'''
#通过邮件发送IP地址 
'''

if __name__ == '__main__':
    iptxt = get_ip_address()
    ip_save_file(iptxt)          
    ip_send_mail(iptxt)