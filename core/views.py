from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core import forms

def profile(request):
    form = profile_form.ProfileForm()
    return render(request, 'profile.html', {'form': form})
    

def index(request):
    return HttpResponse("Hello, world. Novikov <3.")