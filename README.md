# Get-ip-address via email
python脚本自动获取本机ip，并发送到邮箱。适应linux系统和树莓派（raspberry pi）


## 功能组成：
- get_ip_address.py ，主程序，包含以下三个内容：
  + get_ip_address():获取所有接口的ip
  + ip_save_file():把获取到的ip存入文件（后续想在raspberry pi上通过蓝牙获取ip）
  + ip_send_mail():把获取的IP发送到指定邮箱
-config.py，邮件账户配置文件

## 使用说明
 - 先在config里面设置好收发的邮箱地址和账号信息，以及SMTP服务器地址和端口。
 - 运行环境<=python 2.7


## 运行
python get_ip_address.py
