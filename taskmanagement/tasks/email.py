from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class SendEmail:
    def __init__(self):
        self.EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    
    def send_email(self,email_title,email_template,user_email):
        email = EmailMessage(
                email_title,  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [user_email]  # 收件者
            )
        email.fail_silently = False
        email.send()

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
