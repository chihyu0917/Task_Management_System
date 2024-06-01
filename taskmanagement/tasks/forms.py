#from django import forms
#from django.contrib.auth.models import User
#from .models import Event, SharedEvent
#from .models import CustomUser

#class ShareEventForm(forms.Form):
#    event_id = forms.IntegerField(widget=forms.HiddenInput())
#    shared_with = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Share with")

#    def save(self, user):
#        event = Event.objects.get(id=self.cleaned_data['event_id'])
#        shared_with_user = self.cleaned_data['shared_with']
#        SharedEvent.objects.create(event=event, shared_with=shared_with_user, shared_by=user)
from django import forms

class ShareEventForm(forms.Form):
    shared_with = forms.CharField(label='Share with (username)', max_length=150)
