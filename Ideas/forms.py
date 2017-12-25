from django import forms

from .models import Idea


class IdeaForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    def save(self):
        new_task = Idea()
        new_task.name = self.cleaned_data['title']
        new_task.description = self.cleaned_data['description']
        new_task.slugcreator()
        new_task.save()
        return new_task
