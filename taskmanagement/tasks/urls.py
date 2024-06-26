from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views, statistics, auth_views, reminder, pomodoro, calendar,share
#from .views import event_list_for_sharing, share_event, shared_events

# from tasks import auth_views
urlpatterns = [
    path('', views.JumpToPage.tocreate_event, name = 'tasks'),
    path('create_event/', views.EventManager.create_event),
    path('toupdate_event/', views.JumpToPage.toupdate_event),
    path('update_event/', views.EventManager.update_event),
    path('todelete_event/', views.JumpToPage.todelete_event),
    path('delete_event/', views.EventManager.delete_event),
    path('categories/', views.EventManager.categorized_events),
    path('search/', views.EventManager.search_events),
    # path('list_event/', views.EventManager.list_event),
    path('week_events/', views.EventManager.week_events),
    path('event/<int:event_id>/', views.EventManager.update_event_detail, name='event-detail'),
    path('create_chart/', statistics.StatisticManager.createChart, name='create_chart'),
    path('list_users/', views.list_users, name='list_users'),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('user-ranking/', views.user_ranking_by_last_login, name='user-ranking'),
    path('todo/',auth_views.todo_list, name='todo_list'),
    path('diary/',auth_views.diary_list, name='diary_list'),
    path('update_task/<int:task_id>/', auth_views.update_task, name='update_task'),
    path('diary/delete/<int:entry_id>/', auth_views.delete_entry, name='delete_entry'),
    path('pomodoro/', pomodoro.pomodoro_timer, name='pomodoro_timer'),
    path('calendar/', calendar.calendar_view, name='calendar'),
    path('calendar_list/', calendar.event_list, name='calendar_list'),
    path('event_list_for_sharing/', share.event_list_for_sharing, name='event-list-for-sharing'),
    path('shared_events/', share.shared_events, name='shared-events'),
    path('share_event/<int:event_id>/', share.share_event, name='share-event'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
