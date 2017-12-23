from django import forms
from .models import Task

from People.models import People

class TaskForm(forms.Form):
    name = forms.CharField(max_length=50)
    user = forms.ModelChoiceField(queryset=People.objects.filter(activated=True))
    date = forms.DateField(widget=forms.SelectDateWidget)

    def save(self):
        new_task = Task()
        new_task.name = self.cleaned_data['name']
        new_task.user = self.cleaned_data['user']
        new_task.date = self.cleaned_data['date']
        new_task.saveslug(self.cleaned_data['name'])
        new_task.save()
        return new_task
