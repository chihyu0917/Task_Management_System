from django.db import models
from django.conf import settings
from tasks.userinfo import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True) #this is the primary key to identify the event
    name = models.CharField(max_length=100) #this is the name of the event
    label = models.CharField(max_length=100) #this is the label of the event, it is used to categorize the event
    date = models.DateField() #this is the date of the event
    description = models.CharField(max_length=255, blank=True)
#    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
#    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')  

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

class SharedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_events')
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_by')
#    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_events')
#    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event} shared by {self.shared_by} with {self.shared_with}"

class Chat(models.Model):
    #settings.AUTH_USER_MODEL
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.sender} to {self.receiver} at {self.timestamp}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



