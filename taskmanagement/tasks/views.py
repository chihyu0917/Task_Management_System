from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django import forms
from . models import Event, Friendship, SharedEvent, Chat
from datetime import datetime
from .week_events import WeekEvents
from .userinfo import CustomUser, CustomUserManager, UserAuthForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Event, SharedEvent, CustomUser
from .forms import ShareEventForm, MessageForm
#from .chat import chat_room
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

class JumpToPage:
    @staticmethod
    def get_all_events():
        return Event.objects.all()
    def tocreate_event(request):
        return render(request, 'create_event.html')
    def toupdate_event(request):
        events = JumpToPage.get_all_events()
        return render(request, 'update_event.html', {'events': events})
    def todelete_event(request):
        events = JumpToPage.get_all_events()
        return render(request, 'delete_event.html', {'events': events})
    

class EventManager:
    @staticmethod
    def create_event(request):
        if request.method == 'POST':
            name = request.POST.get('event_name')
            label = request.POST.get('event_label')
            date = request.POST.get('event_date')
            if name and label and date:
                Event.objects.create(name=name, label=label, date=date)
                return HttpResponse("Event創建成功。")
            else:
                return HttpResponse("Event創建失敗。")
        else:
            pass

    def update_event(request):
        if request.method == 'POST':
            name = request.POST.get('event_name')
            label = request.POST.get('event_label')
            date = request.POST.get('event_date')

            event_id = request.POST.get('event_id')

            if not (name or label or date):
                return HttpResponse("請輸入更新的內容！")
            else:
                event = get_object_or_404(Event, pk=event_id)
                if name:
                    event.name = name
                if label:
                    event.label = label
                if date:
                    event.date = date
                event.save()
            return HttpResponse("修改成功！")
        else:
            return HttpResponse("修改失敗！")

    def delete_event(request):
        if request.method == 'POST':
            event_ids = request.POST.getlist('events') #取得checkbox的id
            if event_ids:
                for event_id in event_ids:
                    Event.objects.filter(id=event_id).delete()
                return HttpResponse("已成功删除")
            else:
                return HttpResponse("删除失敗！")
        else:
            pass

    def categorized_events(request):
        labels = Event.objects.values_list('label', flat=True).distinct()
        categorized_events = {}
        for label in labels:
            events = Event.objects.filter(label=label)
            categorized_events[label] = events
        return render(request, 'categorized_events.html', {'categorized_events': categorized_events})

    def search_events(request):
        if request.method == 'GET':
            search_label = request.GET.get('event_label')
            if search_label:
                events = Event.objects.filter(label__icontains=search_label)
                if events:
                    response = "<br>".join([f"{event.name} - {event.label} - {event.date}" for event in events])
                    return HttpResponse(response)
                else:
                    return HttpResponse("沒有找到！請重新輪入")
            else:
                return HttpResponse("空白內容！")
        else:
            pass
            
    # def list_event(request):
    #     events = Event.objects.all()
    #     return render(request, 'list_event.html', {'events': events})
    
    def update_event_detail(request, event_id):
        if request.method == 'POST':
            event = get_object_or_404(Event, pk=event_id)
            event.description = request.POST.get('event_description')
            event.save()
            return HttpResponse("更新成功！")
        else:
            event = get_object_or_404(Event, pk=event_id)
            return render(request, 'event_detail.html', {'event': event})


    def week_events(request):
        current_date = datetime.now().date()
        all_events = Event.objects.all().order_by('date')

        events_by_week = {}
        for event in all_events:
            week_number = WeekEvents.get_week_number(event.date)
            if week_number not in events_by_week:
                events_by_week[week_number] = []
            events_by_week[week_number].append(event)

        weeks_data = []
        for week_number, events in events_by_week.items():
            week_start, week_end = WeekEvents.get_week_range_for_number(current_date.year, week_number)
            week_title = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
            weeks_data.append({'week_title': week_title, 'events': events})

        return render(request, 'week_events.html', {'weeks_data': weeks_data})

# class FriendManager:
def friend_list(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    print(user)
    friendships = Friendship.objects.filter(user=user)
    friends = [friendship.friend for friendship in friendships]
    return render(request, 'friend_list.html', {'friends': friends})

def add_friend(request, friend_id):
    user = CustomUser.objects.get(id=request.session['user_id'])
    friend = CustomUser.objects.get(id=friend_id)
    if user == friend:
        return HttpResponse("不能關注自己為好友！")
    elif Friendship.objects.filter(user=user, friend=friend).exists():
        return HttpResponse("已經是關注的好友！")
    Friendship.objects.create(user=user, friend=friend)
    return redirect('friend_list')

def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'list_users.html', {'users': users})

def user_ranking_by_last_login(request):
    users = CustomUser.objects.all().order_by('-last_login')
    return render(request, 'user_ranking.html', {'users': users})

def event_list_for_sharing(request):
    events = Event.objects.all()
    return render(request, 'event_list_for_sharing.html', {'events': events})

import logging

logger = logging.getLogger(__name__)

@login_required
def chat_list(request):
    shared_events = SharedEvent.objects.filter(shared_by=request.user)
    shared_users = {se.shared_with for se in shared_events}
    customusers = CustomUser.objects.all()
#    print(shared_users)
#    print(customusers)
    return render(request, 'chat_list.html', {'shared_users': shared_users, 'customusers': customusers})
    #custom_user = CustomUser.objects.get(username=shared_users)
    #return render(request, 'chat_list.html', {'custom_user_id': custom_user.id})

'''
def chat_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = Chat.objects.filter(
        sender=request.user,
        receiver=other_user
    ) | Chat.objects.filter(
        sender=other_user,
        receiver=request.user
    ).order_by('timestamp')
    form = MessageForm()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = other_user
            chat.save()
            return redirect('chat_detail', user_id=user_id)

    return render(request, 'chat_detail.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form,
    })
'''

def chat_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    
    # 获取当前用户与指定用户之间的聊天消息
    messages = Chat.objects.filter(
        sender=request.user,
        receiver=other_user
    ) | Chat.objects.filter(
        sender=other_user,
        receiver=request.user
    ).order_by('timestamp')
    
    # 显示发送消息的表单
    form = MessageForm()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = other_user
            chat.save()
            return redirect('chat_detail', user_id=user_id)

    return render(request, 'chat_detail.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form,
    })