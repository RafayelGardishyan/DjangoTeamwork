from django import forms

from .models import Short


class ShortForm(forms.Form):
    path = forms.SlugField(max_length=100)
    url = forms.URLField(widget=forms.URLInput)

    def save(self):
        newshort = Short()
        newshort.slug = self.cleaned_data['path']
        newshort.link = self.cleaned_data['url']
        newshort.save()
