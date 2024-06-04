from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, SharedEvent, Chat
from django.contrib.auth.models import User
from .forms import ShareEventForm
from .models import CustomUser
from .forms import MessageForm

@login_required
def event_list_for_sharing(request):
    events = Event.objects.all()
    return render(request, 'event_list_for_sharing.html', {'events': events})

@login_required
def shared_events(request):
    shared_events = SharedEvent.objects.filter(shared_with=request.user)
    return render(request, 'shared_events.html', {'shared_events': shared_events})

@login_required
def share_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = ShareEventForm(request.POST)
        if form.is_valid():
            shared_with_username = form.cleaned_data['shared_with']
            shared_with = CustomUser.objects.get(username=shared_with_username)
            SharedEvent.objects.create(event=event, shared_by=request.user, shared_with=shared_with)
            return redirect('shared-events')
    else:
        form = ShareEventForm()
    return render(request, 'share_event.html', {'form': form, 'event': event})
'''
@login_required
def chat_list(request):
    shared_events = SharedEvent.objects.filter(shared_by=request.user)
    shared_users = {se.shared_with for se in shared_events}
    return render(request, 'chat_list.html', {'shared_users': shared_users})

@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = other_user
            chat.save()
            return redirect('chat_detail', user_id=user_id)
    else:
        form = MessageForm()
    messages = Chat.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    return render(request, 'chat_detail.html', {
        'form': form,
        'messages': messages,
        'other_user': other_user
    })
    '''