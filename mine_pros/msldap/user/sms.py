import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


class SendEmail(object):
    def __init__(self):
        self.server = {'name': '10.211.16.33',
                       'user': 'ldap',
                       'passwd': '2qazxsw3CDE$'}
        self.fro = 'ldap@eptok.com'

    def verify_code(self):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        msg_code = ''.join(x)
        return msg_code

    # server['name'], server['user'], server['passwd']
    def send_mail(self, to, subject="", text="", files=[]):
        assert type(to) == list
        assert type(files) == list

        msg = MIMEMultipart()
        msg['From'] = self.fro  # 邮件的发件人
        msg['Subject'] = subject  # 邮件的主题
        msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
        msg['Date'] = formatdate(localtime=True)  # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
        # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        for file in files:  # 添加附件可以是多个，files是一个列表，可以为空
            part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
            with open(file, 'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)

        smtp = smtplib.SMTP()
        # smtp = smtplib.SMTP_SSL()  # 使用SSL的方式去登录(例如QQ邮箱，端口是465)
        smtp.connect(self.server['name'])  # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
        smtp.login(self.server['user'], self.server['passwd'])  # 用户名，密码
        smtp.sendmail(self.fro, to, msg.as_string())  # 发件人，收件人，发送信息
        smtp.close()  # 关闭连接


if __name__ == '__main__':
    pass
    # send_mail(server, fro, to, subject, text)
    # sm = SendEmail()
    # sm.send_mail(['120430105@qq.com'], 'test04', 'verify code04')

