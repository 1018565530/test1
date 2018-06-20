#!/usr/bin/envpython
#encoding=utf-8
import difflib
import string
import smtplib
from email.mime.text import MIMEText

host = 'smtp.163.com'
subject = 'test'
form = 'yikunge1@163.com'
to = '1118565530@qq.com'
text = 'python rules them all!'
body = string.join((
    "From: %s"  % form,
    "To: %s" % to,
    "Subject:% s" % subject,
    "",
    text
),"\r\n")
server = smtplib.SMTP()
server.connect('smtp.163.com',"25")
server.starttls()
server.login("form","pass")
server.sendmail(form,to,body)
server.quit()
