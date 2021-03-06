from django.http import JsonResponse
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
import random, string
from dal import autocomplete

class GroupAutoCompleteView(ModelGroup):
    def get(self,request,*args,**kwargs):
        data = request.GET
        number = data.get("term")
        if number:
            groups = ModelGroup.objects.filter(number__icontains= number)
        else:
            groups = ModelGroup.objects.all()
            results = []
        for group in groups:
            group_json = {}
            group_json['id'] = group.id
            group_json['label'] = group.number
            group_json['value'] = group.number
            results.append(group_json)
            data = json.dumps(results)
            mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class GroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ModelGroup.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

def my_timetable(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    user = UserProfile.objects.get(user=request.user)
    user_courses = list(Course.objects.filter(users_allowed=user))
    if user.is_lecturer:
        user_courses += list(Course.objects.filter(groups_allowed=user.group_key))
    user_courses = ModelCourse.objects.all()[:5]
    return render(request, 'timetable.html', {'courses': user_courses},  RequestContext(request))

def get_timetable(request):
    timestamp = request.GET.get('at', '')
    user = UserProfile.objects.get(user=request.user)
    user_courses = list(ModelCourse.objects.filter(users_allowed=user))
    if user.is_lecturer:
        user_courses += list(ModelCourse.objects.filter(groups_allowed=user.group_key))
    data = []
    for c in user_courses:
        data += ModelClassFormat.objects.filter(course=c)
    return JsonResponse(data, safe=False)

def create_gr(request):
    print(request.POST['create_gr'])
    return render(request, 'profile_read.html', {'output': "success"})

def profile_read(request):
    profile = UserProfile.objects.get(user=request.user)
    e = list(ModelGroup.objects.values("number"))
    lst = list(map(lambda x: x['number'], e))

    if request.user.is_authenticated() == False:
        return render(request, 'index.html')

    # if request.method == 'POST':
    #     print(c.id)
    #     profile.group_key = lst[request.POST['create_gr']]
    #     profile.save()
    #     return HttpResponseRedirect('/profile')
    print(lst)
    return render(request, 'profile_read.html', {'user': profile, 'grs':lst},  RequestContext(request))

def profile_edit(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':

        profile = UserProfile.objects.get(user=request.user)
        profile.first_name = request.POST["first_name"]
        profile.middle_name = request.POST.get("middle_name", "")
        profile.last_name = request.POST["last_name"]
        profile.phone_number = request.POST.get("phone_number", "")
        if profile.is_lecturer:
            profile.degree = request.POST.get("degree", "")

        profile.save()
        return HttpResponseRedirect('/profile')
    form = UserProfileForm(instance = profile)
    if not profile.is_lecturer:
        del form.fields["degree"]
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
        first_name = request.POST["first_name"]
        try:
            user = User(username=email,email=email,first_name=first_name)
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
            profile.save()

            #group = Group(number = "100/1")
            #group.starosta_id = profile

            #group.save()

            form = ProfileRegistrationForm()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = ProfileRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def create_course(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    if request.method == 'POST':
        print("create_course post")
        name = request.POST.get('name', '')
        report_type = request.POST.get('report_type', '')
        beginning_date = request.POST.get('beginning_date', '')
        ending_date = request.POST.get('ending_date', '')
        ending_date = request.POST.get('ending_date', '')
        new_subj = Subject(name=name)
        new_subj.save()
        new_course = Course(name=name, subject=new_subj, report_type=report_type, beginning_date=beginning_date, ending_date=ending_date)
        new_course.save()
        profile = UserProfile.objects.get(user=request.user)
        if not profile.is_lecturer:
            new_course.groups_allowed.add(profile.group)
        new_course.users_allowed.add(profile)
        return redirect('my_courses')
    else:
        form = CourseEditForm()
    return render(request, 'cource_form.html', {'form': form})

def group_create(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    if request.method == 'POST':
        number = request.POST.get('number', '')
        group = Group(starosta_id=profile, number=number)
        group.save()
        profile.group_key = group
        profile.save()
        return HttpResponseRedirect('/list_of_groups')

    profile = UserProfile.objects.get(user=request.user)
    form = GroupForm()
    return render(request, 'group_form.html', {'form': form})

def view_courses(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    courses = ModelCourse.objects.all()
    user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        for c in courses:
            if request.POST.get(c.name):
                c.users.add(user)
                c.save()

    return render(request, 'list_of_courses.html', {'courses': courses, 'user': user})

def view_groups(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    groups = Group.objects.all()
    user = UserProfile.objects.get(user=request.user)
    return render(request, 'list_of_groups.html', {'groups': groups, 'user': user})

def view_group_information(request, pk):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')
    user = UserProfile.objects.get(user=request.user)
    group = Group.objects.get(id=pk)
    group_list = UserProfile.objects.filter(group_key=group).all()

    if request.method == 'POST':
        if request.POST.get('generate_code'):
            new_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            secret_code = SecretCode(code=new_code)
            secret_code.save()
            return render(request, 'group_info.html', {'pk': pk, 'group': group, 'group_list': group_list, 'user': user, 'code': new_code})

        user.group_key = None
        user.save()
        return HttpResponseRedirect('/profile')


    return render(request, 'group_info.html', {'pk': pk, 'group': group, 'group_list': group_list, 'user': user})

def view_safety_code(request, pk):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')

    if request.method == 'POST':
        code = request.POST.get('code', '')
        try:
            get_code = SecretCode.objects.get(code=code)
        except SecretCode.DoesNotExist:
            form = SafetyCodeForm()
            return render(request, 'safety_code.html', {'form': form, 'wrong': True})
        get_code.delete()
        user = UserProfile.objects.get(user=request.user)
        group = Group.objects.get(id=pk)
        user.group_key = group
        user.save()
        return HttpResponseRedirect('/profile')

    form = SafetyCodeForm()
    return render(request, 'safety_code.html', {'form': form})

def view_my_courses(request):
    if request.user.is_authenticated() == False:
        return render(request, 'index.html')

    user = UserProfile.objects.get(user=request.user)
    user_courses = list(Course.objects.filter(users_allowed=user))
    if user.is_lecturer:
        user_courses += list(Course.objects.filter(groups_allowed=user.group_key))

    if request.method == 'POST':
        for c in user_courses:
            if request.POST.get(c.name):
                c.users.remove(user)
                c.save()

    return render(request, 'my_courses.html', {'courses': user_courses})

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

def view_help_reg(request):
    return render(request, 'help_reg.html')

def view_help_unreg(request):
    return render(request, 'help_unreg.html')

def index(request):
    return HttpResponse("Unauthorized.")
