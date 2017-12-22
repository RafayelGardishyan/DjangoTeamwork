from django import forms

from .models import Plan


class PlanForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    deadline = forms.DateField()

    def save(self):
        new_task = Plan()
        new_task.name = self.cleaned_data['name']
        new_task.description = self.cleaned_data['description']
        new_task.deadline = self.cleaned_data['deadline']
        new_task.slugcreator()
        new_task.save()
        return new_task
