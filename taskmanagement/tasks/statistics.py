from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from collections import Counter
import json


class StatisticManager:
    @staticmethod
    def createChart(request):
        chart_type = request.POST.get('chart_type', 'pie')  # 從 POST 請求中獲取圖表類型，預設為餅圖
        labels = Event.objects.values_list('label', flat=True).distinct()
        statistics_events = Counter()

        for label in labels:
            count = Event.objects.filter(label=label).count()
            statistics_events[label] = count

        labels = list(statistics_events.keys())
        data = list(statistics_events.values())

        context = {
            'labels': json.dumps(labels),
            'data': json.dumps(data),
            'chart_type': chart_type
        }

        return render(request, 'statistics.html', context)

