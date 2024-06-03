# from datetime import datetime
# from django.shortcuts import render
# from tasks.models import Event
# from tasks.email import SendEmail


# # Create your views here.
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job,DjangoResultStoreMixin
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string

# # 实例化调度器
# scheduler = BackgroundScheduler()
# # 开启定时工作
# # 调度器使用DjangoJobStore()
# scheduler.add_jobstore(DjangoJobStore(), "default")

# user = []

# # 设置定时任务，选择方式为interval，时间间隔为10s
# # 另一种方式为每天固定时间执行任务，对应代码为：
# # @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='18', minute='50', second='10',id='task_time')
# @register_job(scheduler, 'cron', hour='05', minute='30',id='test', replace_existing=True)
# def my_job1():
#     # 这里写你要执行的任务

#     current_date = datetime.now().date()
#     events = Event.objects.filter(date = current_date)
#     # user = CustomUser.objects.filter(id = 1)
#     # user_email = user.email
#     # useremail = SendEmail.EmailAdd
#     # user = []
#     # user.append(useremail)
    

#     # print(SendEmail.EmailAdd)

#     if events is not None:

#         email_template = render_to_string(
#                 'reminder_email.html',
#                 {'events': events}
#              )
        
#         email = EmailMessage(
#                 '今日行程提醒',  # 電子郵件標題
#                 email_template,  # 電子郵件內容
#                 settings.EMAIL_HOST_USER,  # 寄件者
#                 [user[0]]  # 收件者
#                 )
#         email.fail_silently = False
#         email.send()
#     pass


# # register_events(scheduler)    最新的django_apscheduler已经不需要这一步
# # scheduler.start()


# @register_job(scheduler, "interval", seconds=10, replace_existing=True)  # replace_existing=解决第二次启动失败的问题
# def my_job():
#     # 这里写你要执行的任务

#     # current_date = datetime.now().date()
#     # events = Event.objects.filter(date = current_date)
#     # user = CustomUser.objects.filter(id = 1)
#     # user_email = user.email
#     useremail = SendEmail.EmailAdd
#     # user = []
#     if (useremail != ''):
#         user.append(useremail)
    
        
    
    

#     # print(SendEmail.EmailAdd)

#     # email_template = render_to_string(
#     #             'reminder_email.html',
#     #             {'events': events}
#     #         )
        
#     # email = EmailMessage(
#     #             '今日行程提醒',  # 電子郵件標題
#     #             email_template,  # 電子郵件內容
#     #             settings.EMAIL_HOST_USER,  # 寄件者
#     #             [user[0]]  # 收件者
#     #         )
#     # email.fail_silently = False
#     # email.send()
#     pass


# # register_events(scheduler)    最新的django_apscheduler已经不需要这一步
# scheduler.start()
