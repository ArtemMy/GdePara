from django import forms
from django.utils import timezone

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    def __str__(self):
        return self.title