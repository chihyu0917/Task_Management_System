from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class SendEmail:

    EmailAdd = ''

    def __init__(self,emailadd = None):
        self.EMAIL_HOST_USER = settings.EMAIL_HOST_USER
        self.emailadd  = self.EmailAdd 

    # def set_email(email):
    #      = email
    
    def send_register_mail(self,user,user_email):
        
        email_template = render_to_string(
                'signup_success_email.html',
                {'username': user}
            )
        
        email = EmailMessage(
                '註冊成功通知信',  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [user_email]  # 收件者
            )
        email.fail_silently = False
        email.send()
        # self.EmailAdd = user_email
        
        self.emailadd = user_email


    def reminder(self):
        email_template = render_to_string(
                'signup_success_email.html',
                {'username': 'abcnd'}
            )
        
        email = EmailMessage(
                '註冊成功通知信2',  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [self.emailadd]  # 收件者
            )
        email.fail_silently = False
        email.send()
        # self.EmailAdd = user_email
        # # self.emailadd = user_email
        # print(self.emailadd)

    
