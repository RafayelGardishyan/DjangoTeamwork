from django import forms

from .models import Log
from People.models import People

class LogForm(forms.Form):
    title = forms.CharField(max_length=100)
    user = forms.ModelChoiceField(queryset=People.objects.all())
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        new_task = Log()
        new_task.title = self.cleaned_data['title']
        new_task.text = self.cleaned_data['text']
        new_task.user = self.cleaned_data['user']
        new_task.slugcreator()
        new_task.save()
        return new_task
