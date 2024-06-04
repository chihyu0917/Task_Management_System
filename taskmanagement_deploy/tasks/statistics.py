from django.shortcuts import render
from .models import Event
from collections import Counter
import json

class Chart:
    def __init__(self, chart_type='pie'):
        self.chart_type = chart_type
        self.labels = []
        self.data = []

    def load_data(self):
        labels = Event.objects.values_list('label', flat=True).distinct()
        statistics_events = Counter()

        for label in labels:
            count = Event.objects.filter(label=label).count()
            statistics_events[label] = count

        self.labels = list(statistics_events.keys())
        self.data = list(statistics_events.values())

    def get_context(self):
        self.load_data()
        return {
            'labels': json.dumps(self.labels),
            'data': json.dumps(self.data),
            'chart_type': self.chart_type
        }

class StatisticManager:
    @staticmethod
    def createChart(request):
        chart_type = request.POST.get('chart_type', 'pie')
        chart = Chart(chart_type)
        context = chart.get_context()
        return render(request, 'statistics.html', context)
