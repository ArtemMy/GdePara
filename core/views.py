from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core.forms import LoginForm, ProfileRegistrationForm
from core.models import UserProfile, Group
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError

def profile_read(request):
    user = UserProfile(request.user)
    if request.user.is_authenticated():
        return render(request, 'profile_read.html', {'user': user})
    else:
        return render(request, 'index.html')

def profile_edit(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        form = LoginForm()
        if(user == None):
            return render(request, 'login.html', {'form': form, 'error' : "wrong email or password"})
        else:
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def SignupView(request):
    if request.method == 'POST':
        email = request.POST['email']
        UserModel = get_user_model()
        try:
            user = User(username=email,email=email)
            user.set_password(request.POST['password'])
            user.save()
#            user = UserModel.objects.get(username=email)
        except IntegrityError:
            form = ProfileRegistrationForm()
            return render(request, 'signup.html', {'form': form, 'error' : "email already taken"})
        else:
            profile = UserProfile(user = user)
            profile.is_lecturer = bool(request.POST["is_lecturer"])
            profile.first_name = request.POST["first_name"]
            profile.middle_name = request.POST["middle_name"]
            profile.last_name = request.POST["last_name"]
            profile.phone_number = request.POST["phone_number"]
            profile.email = request.POST["email"]
            profile.degree = request.POST["degree"]
            profile.save()

            group = Group(number = "100/1")
            group.starosta_id = profile

            group.save()

            form = ProfileRegistrationForm()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = ProfileRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return HttpResponse("Hello, world. Novikov <3.")