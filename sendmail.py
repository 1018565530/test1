#!/usr/bin/envpython
#encoding=utf-8
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


host = 'smtp.163.com'
subject = 'test'
form = 'yikunge1@163.com'
to = '1018565530@qq.com'
text = 'python rules them all!'

def addimg(src,imgid):
    fp = open(src,'rb')
    msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID',msgid)
    return msgImage
msg = MIMEMultipart('related')
msgtext = MIMEText("<font color=red>111<br><img src=\"cid:weekly\"></font>",'html','utf-8')
msg.attach(msgtext)
msg.attach(addimg("img/weekly.png","weekly"))
attach = MIMEText(open("doc/week_report.xlsx","rb").read(),"base64","utf-8")
attach["Content-Type"] = "application/octet-stream"


msg.attach(attach)
msg['subject'] = subject
msg['form'] = form
msg['to'] = to
try:
    server = smtplib.SMTP()
    server.connect('smtp.163.com',"25")
    server.starttls()
    server.login("yikunge1@163.com","xxx")
    server.sendmail(form,to,body)
    server.quit()
    print success
except Exception as e:
    print str(e)
