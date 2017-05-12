from django import forms
from django.utils import timezone
from registration.forms import RegistrationFormUniqueEmail
 
class ProfileRegistrationForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    is_lecturer = forms.BooleanField(label = "Are you lecturer?:")
    first_name = forms.CharField(max_length=30)
    middle_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=30)
    degree = forms.CharField(max_length=30)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    def __str__(self):
        return self.title