#!/usr/bin/env python
# -*- coding: utf-8 -*-
#version <= python 2.7
#__author__ = 'Page Wong'

import array
import struct
import socket
import fcntl
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

def get_ip_address():
    '''
    #获取IP地址功能# 
    '''

    #先获取所有网络接口
    SIOCGIFCONF = 0x8912
    SIOCGIFADDR = 0x8915
    BYTES = 4096         
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B',b'\0' * BYTES)
    bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]
    namestr = names.tostring()
    ifaces = [namestr[i:i+32].split('\0', 1)[0] for i in range(0, bytelen, 32)]
    
    #再获取每个接口的IP地址
    iplist = []
    for ifname in ifaces:
        ip = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),SIOCGIFADDR,struct.pack('256s',ifname[:15]))[20:24])
        iplist.append(ifname+':'+ip)
    return iplist

    
def ip_save_file(iptxt):
    '''
    #存入IP地址到文件#
    直接发邮件不需读取次文件
    后续通过其它途径传送IP地址时用到 
    '''

    #获取当前时间，因为每次启动IP都在变，记录上时间容易区分
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #写入文件
    with open('ipaddress.txt','w') as f:
        f.write(now+'\r\n')
        for ip in get_ip_address(): 
            f.write(ip+'\r\n')

            
def ip_send_mail(iptxt):
    '''
    #发送IP地址到制定邮箱#
    '''
    #导入邮件账户配置文件
    import config as mail
    
    fromaddr = mail.fromaddr
    toaddrs = mail.toaddrs
    username = mail.username
    password = mail.password
    server = smtplib.SMTP(mail.smtp_sever)
    
    #设置邮件正文，get_ip_address()返回的是list，要转换成str
    ip = '\r\n'.join(iptxt)
    
    #设置邮件标题和正文
    msg = MIMEText(ip,'plain', 'utf-8')
    msg['Subject'] = 'IP For RaspberryPi'
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    
    #启动SMTP发送邮件
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def main():
    '''
    #程序入口#
    '''

    #获取IP
    iptxt = get_ip_address()
    
    #将IP存入文件，如果直接发送邮件，这步可以省略。
    ip_save_file(iptxt)
    
    #将IP地址发送到指定邮箱
    ip_send_mail(iptxt)

if __name__ == '__main__': 
    '''
    #运行
    '''   
    main()