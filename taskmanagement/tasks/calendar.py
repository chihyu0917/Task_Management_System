from django.shortcuts import render
from django.http import JsonResponse
from .models import Event

def calendar_view(request):
    # events = Event.objects.all()
    # events_json = [
    #     {
    #         'name': event.name,            
    #         'date': event.date.isoformat()
    #     } for event in events
    # ]


    # return render(request, 'calendar.html', {'events_json': events_json})
    return render(request, 'calendar.html')

def event_list(request):
    events = Event.objects.all()
    # events_json = [
    #     {
    #         'name': event.name,            
    #         'date': event.date.isoformat()
    #     } for event in events
    # ]

    events_json = []
    for event in events:
        events_json.append({
            'title': event.name,
            'start': event.date.isoformat(),
            'end': event.date.isoformat(),
        })

    return JsonResponse(events_json, safe=False)