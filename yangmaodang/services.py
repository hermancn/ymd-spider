# coding:utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time


def send_email(filename):
    _user = "aihaoyangmao@sina.com"
    _pwd  = "yangmaodang"
    _to   = "aihaoyangmao@163.com"

    #如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg["Subject"] = 'newsmth-'+time.strftime('%Y%m%d')
    msg["From"]    = _user
    msg["To"]      = _to

    #---这是文字部分---
    part = MIMEText(u"庞老师辛苦！", 'plain', 'utf-8')
    msg.attach(part)

    #---这是附件部分---
    if os.path.isfile(filename):
        part = MIMEApplication(open(filename, 'rb').read())
        part.add_header('Content-Disposition', 'attachment',
                        filename=filename)
        msg.attach(part)

    s = smtplib.SMTP("smtp.sina.com", timeout=30)#连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)#登陆服务器
    s.sendmail(_user, _to, msg.as_string())#发送邮件
    s.close()
