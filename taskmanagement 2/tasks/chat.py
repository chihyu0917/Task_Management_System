# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm

@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=form.cleaned_data['content']
            )
            return redirect('chat-room', chat_id=chat_id)
    else:
        form = MessageForm()
    return render(request, 'chat_room.html', {'chat': chat, 'form': form})
