from django import forms
from .models import Task

from People.models import People

class TaskForm(forms.Form):
    name = forms.CharField(max_length=50)
    user = forms.ModelChoiceField(queryset=People.objects.all())
    date = forms.DateField()

    def save(self):
        new_task = Task.objects.create(
            name=self.cleaned_data['name'],
            user=self.cleaned_data['user'],
            date=self.cleaned_data['date'],
        )
        return new_task
