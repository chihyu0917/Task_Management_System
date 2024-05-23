from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .userinfo import CustomUser


class SendEmail:

    EmailAdd = ''

    def __init__(self,emailadd = None):
        self.EMAIL_HOST_USER = settings.EMAIL_HOST_USER
        self.emailadd  = '' 

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
        SendEmail.EmailAdd = user_email

    def getemail(self,username):
        user = CustomUser.objects.get(username=username)
        user_email = user.email
        SendEmail.EmailAdd = user_email
        # self.emailadd = user_email


    def reminder(self):

        # user_email = CustomUser.email.__get__
        # user = CustomUser.objects.get(username=username)
        # user = CustomUser.objects.get
        # user_email = user.email

        email_template = render_to_string(
                'signup_success_email.html',
                {'username': 'abcnd'}
            )
        
        email = EmailMessage(
                '註冊成功通知信2',  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [SendEmail.EmailAdd]  # 收件者
            )
        email.fail_silently = False
        email.send()
        # print(SendEmail.EmailAdd)
        # self.EmailAdd = user_email
        # # self.emailadd = user_email
        # print(self.emailadd)

    def send_email_reminder(self,
                            username,
                            orderno,
                            products,
                            created_time,
                            status,
                            user_email):
        email_template = render_to_string(
            'orders/createorder.html',
            {
                "username":username,
                "orderno":orderno,
                "products":products,
                "created_time":created_time,
                "status":status
            }
        )

        email = EmailMessage(
            "鍵盤貿易 - 訂單建立成功通知信",
            email_template,
            self.EMAIL_HOST_USER,
            [user_email]
        )
        email.content_subtype = 'html'
        email.fail_silently = False
        email.send()

    def corn_job():
        print("This is cronjob test")


