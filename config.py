#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version <= python 2.7
#__author__ = 'Page Wong'

if __name__ == '__main__': 
    print("这是配置文件，不能单独运行")

#设置收件邮箱
toaddrs  = 'to@mail.com'

#设置发送邮箱
fromaddr = 'send@mail.com' 
    
#设置发送邮箱的账号密码
username = 'your_sendmail@mail.com' 
password = 'your_password'
    
#设置SMTP服务器、端口，根据你的邮箱设置，
smtp_sever = 'smtp.mail.com:25'