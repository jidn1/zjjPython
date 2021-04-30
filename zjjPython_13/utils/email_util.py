#!/usr/bin/python3
import smtplib
from email.mime.text import MIMEText


# 常量
mail_host = "smtp.163.com"
mail_user = ""
mail_pass = ""
sender = ''


def sendEmail(title,receivers,content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = '比特吉'
    message['To'] = receivers
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


if __name__ == '__main__':
    sendEmail('比特吉行情提醒','','您好，您关注的火币平台BTC,已低于您设置的: 50231.23价格，目前最新价格为: 49872.78,本次提醒已完成，如需再次提醒，请登录比特吉重新设置价格')