# _*_ encoding:utf-8 _*_
__author__ = 'pig'
__data__ = '2018\7\17 0017 12:05$'

from random import Random
from users.models import EmailVerifRecord
# 导入Django自带的邮件模块
from django.core.mail import send_mail
# 导入设置邮箱信息
from zxptxx.settings import EMAIL_FROM





#生成随机字符串
def random_str(random_length = 8):
    str = ''
    #生成可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str


#发送激活邮件
def send_register_email(email,send_type = "register"):
    # 发送之前先保存到数据库，到时候查询链接是否存在

    #实例化邮箱验证对象
    email_record = EmailVerifRecord()
    #生成随机的code放入链接
    code = random_str(16)
    email_record.code = code
    email_record.email =email
    email_record.send_type = send_type
    email_record.save()

    #自定义邮件内容
    email_title = ""
    email_body = ""

    #判断是否邮件为注册类型
    if send_type == "register":
        email_title = "mtianyan慕课小站 注册激活链接"
        email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)

    # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list,成功返回1
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == "forget":

        email_title = "mtianyan慕课小站 密码重置"
        email_body = "请点击下面的链接重置你的密码:http://127.0.0.1:8000/reset/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list,成功返回1
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass