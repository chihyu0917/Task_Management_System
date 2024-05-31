from django.shortcuts import render

def pomodoro_timer(request):
    return render(request, 'pomodoro.html')