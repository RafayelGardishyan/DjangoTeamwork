from django import forms

from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

    def save(self, commit=True):
        m = super(FileForm, self).save(commit=False)
        m.getname()
        m.saveslug()
        # do custom stuff
        if commit:
            m.save()
        return m