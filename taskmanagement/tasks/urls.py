from django.urls import path

from . import views, statistics
# from tasks import auth_views
urlpatterns = [
    path('', views.JumpToPage.tocreate_event),
    path('create_event/', views.EventManager.create_event),
    path('toupdate_event/', views.JumpToPage.toupdate_event),
    path('update_event/', views.EventManager.update_event),
    path('todelete_event/', views.JumpToPage.todelete_event),
    path('delete_event/', views.EventManager.delete_event),
    path('categories/', views.EventManager.categorized_events),
    path('search/', views.EventManager.search_events),
    # path('list_event/', views.EventManager.list_event),
    path('week_events/', views.EventManager.week_events),
    path('event/<int:event_id>/', views.EventManager.update_event_detail),
    path('create_chart/', statistics.StatisticManager.createChart),
    path('list_users/', views.list_users, name='list_users'),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friend_list/', views.friend_list, name='friend_list'),
]
