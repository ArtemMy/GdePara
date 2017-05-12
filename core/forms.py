from django import forms
from django.utils import timezone
from registration.forms import RegistrationFormUniqueEmail
from core.models import UserProfile
from django.forms import ModelForm

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['is_lecturer'].required = False
        self.fields['first_name'].required = False
        self.fields['middle_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['degree'].required = False
    class Meta:
        model = UserProfile
        fields = ['email', 'is_lecturer', 'first_name', 'middle_name', 'last_name', 'phone_number', 'degree']

class ProfileRegistrationForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    is_lecturer = forms.BooleanField(label = "Are you lecturer?:", initial=True, required=False)
    first_name = forms.CharField(max_length=30)
    middle_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=30,  required=False)
    degree = forms.CharField(max_length=30,  required=False)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    def __str__(self):
        return self.title