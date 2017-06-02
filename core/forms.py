# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone
from registration.forms import RegistrationFormUniqueEmail
from core.models import UserProfile, Course
from django.forms import ModelForm

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True   
        self.fields['email'].label = "Почта"        
        self.fields['is_lecturer'].required = False
        self.fields['is_lecturer'].label = "Преподаватель?"
        self.fields['first_name'].required = False
        self.fields['first_name'].label = "Имя"
        self.fields['middle_name'].required = False
        self.fields['middle_name'].label = "Отчество"
        self.fields['last_name'].required = False
        self.fields['last_name'].label = "Фамилия"
        self.fields['phone_number'].required = False
        self.fields['phone_number'].label = "Телефон"
        self.fields['degree'].required = False
        self.fields['degree'].label = "Степень"
        #self.fields['group_key'].required = False
    class Meta:
        model = UserProfile
        fields = ['email', 'is_lecturer', 'last_name', 'first_name', 'middle_name', 'phone_number', 'degree']

class ProfileRegistrationForm(forms.Form):
	last_name = forms.CharField(label = "Фамилия (*)", max_length=30)
	first_name = forms.CharField(label = "Имя (*)",max_length=30)
	middle_name = forms.CharField(label = "Отчество ",max_length=30, required=False)
	phone_number = forms.CharField(label = "Телефон ",max_length=30,  required=False)
	email = forms.CharField(label = "Почта (*)",max_length=30)
	password = forms.CharField(label = "Пароль (*)",max_length=30)
	####
	confirm_password = forms.CharField(label = "Подтвердите пароль (*)",max_length=30)
	####
	is_lecturer = forms.BooleanField(label = "Преподаватель? ", initial=True, required=False)
	degree = forms.CharField(label = "Степень ",max_length=30,  required=False)

class LoginForm(forms.Form):
    email = forms.CharField(label = "Почта (*)", max_length=30)
    password = forms.CharField(label = "Пароль (*)", max_length=30)

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    def __str__(self):
        return self.title

class GroupForm(forms.Form):
    number = forms.CharField(max_length=150)

class SafetyCodeForm(forms.Form):
    code = forms.CharField(max_length=8)

class CourseEditForm(ModelForm):
    class Meta:
        model = Course;
        fields = ['name', 'report_type', 'beginning_date', 'ending_date']
        widgets = {
            'beginning_date': forms.DateInput(attrs={'class':'datepicker', 'id':'beginning_date'}),
        }
