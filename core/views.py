from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from core.forms import *
from core.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.dispatch import receiver

def profile_read(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.user.is_authenticated():
#        return render_to_response('profile_read.html', RequestContext(request, {'user': profile}))
        return render(request, 'profile_read.html', {'user': profile})
    else:
        return render(request, 'index.html')

def profile_edit(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.is_lecturer = bool(request.POST.get("is_lecturer", False))
        profile.first_name = request.POST["first_name"]
        profile.middle_name = request.POST.get("middle_name", "")
        profile.last_name = request.POST["last_name"]
        profile.phone_number = request.POST.get("phone_number", "")
        profile.email = request.POST["email"]
        profile.degree = request.POST.get("degree", "")

        profile.save()
        return HttpResponseRedirect('/profile')

    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance = profile)
    return render(request, 'profile_edit.html', {'form': form})

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
            profile.is_lecturer = bool(request.POST.get("is_lecturer", False))
            profile.first_name = request.POST["first_name"]
            profile.middle_name = request.POST.get("middle_name", "")
            profile.last_name = request.POST["last_name"]
            profile.phone_number = request.POST.get("phone_number", "")
            profile.email = request.POST["email"]
            profile.degree = request.POST.get("degree", "")
            profile.save()

            #group = Group(number = "100/1")
            #group.starosta_id = profile

            #group.save()

            form = ProfileRegistrationForm()
            login(request, user)
            return HttpResponseRedirect('/index')
    else:
        form = ProfileRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            report_type = request.POST.get('report_type', '')
            beginning_date = request.POST.get('beginning_date', '')
            ending_date = request.POST.get('ending_date', '')
            new_course = Course(name=name, report_type=report_type, beginning_date=beginning_date, ending_date=ending_date)
            new_course.save()
            return redirect('home')
    else:
        form = CreateCourseForm()
    return render(request, 'create_course.html', {'form': form})

def group_create(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    if request.method == 'POST':
        number = request.POST.get('number', '')
        profile = UserProfile.objects.get(user=request.user)
        group = Group(starosta_id=profile, number=number)
        group.save()
        profile.group_id = group.id
        profile.save()
        return HttpResponseRedirect('/list_of_groups')

    profile = UserProfile.objects.get(user=request.user)
    form = GroupForm()
    return render(request, 'group_form.html', {'form': form})

def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'list_of_courses.html', {'courses': courses})

def view_groups(request):
    groups = Group.objects.all()
    return render(request, 'list_of_groups.html', {'groups': groups})

class CourseCreate(CreateView):
    fields = ('name', 'report_type', 'beginning_date', 'ending_date')
    model = Course
    success_url = '/list_of_courses'
    template_name = 'cource_form.html'

class CourseEdit(UpdateView):
    model = Course
    fields = ['name', 'report_type', 'beginning_date', 'ending_date']
    success_url = '/list_of_courses'
    template_name = 'cource_form.html'

class CourseDelete(DeleteView):
    model = Course
    template_name = 'confirm_delete.html'
    success_url = '/list_of_courses'

def index(request):
    return HttpResponse("Hello, world. Novikov <3.")