from django.db import models
from django.utils import timezone
from registration.signals import user_registered
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
import logging

class ModelTeacher(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    degree = models.CharField(max_length=120)

    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

class ModelGroup(models.Model):
    number = models.CharField(max_length=30)
    faculty = models.CharField(max_length=120)
    faculty_abbr = models.CharField(max_length=30)
    spec = models.CharField(max_length=120)
    def get_absolute_url(self):
        return "/group/%i/" % self.id

class ModelCourse(models.Model):
    name = models.TextField()
    teacher = models.ForeignKey(ModelTeacher, null=True)
    groups = models.ManyToManyField(ModelGroup, null=True)
    def get_absolute_url(self):
        return "/course/%i/" % self.id
    def from_model(self):
        return Course(name=self.name, teacher_name=self.teacher.name, model_groups=self.groups)


class ModelClassFormat(models.Model):
    day_of_week = models.IntegerField()
    type_of_class = models.CharField(max_length=254)
    time_of_beginning = models.TimeField()
    time_of_ending = models.TimeField()
    building = models.CharField(max_length=30)
    auditorium = models.CharField(max_length=30)
    week_number = models.IntegerField()
    course = models.ForeignKey(ModelCourse, on_delete=models.CASCADE, null=True)
    def from_model(this, c):
        return ClassFormat(day_of_week=this.day_of_week, course=c,
            type_of_class=this.type_of_class, time_of_beginning=this.time_of_beginning,
            time_of_ending=this.time_of_ending, building=this.building,
            auditorium=this.auditorium, week_number=this.week_number)


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    is_lecturer = models.BooleanField()

    degree = models.CharField(max_length=120)
    # or
    group_key = models.ForeignKey('Group', null=True)

    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

class Subject(models.Model):
    name = models.CharField(max_length=254)
    is_necessary = models.BooleanField(default='True')

class Group(models.Model):
    starosta_id = models.OneToOneField(UserProfile, null=True)
    number = models.CharField(max_length=30)
    faculty = models.CharField(max_length=120)
    faculty_abbr = models.CharField(max_length=30)
    spec = models.CharField(max_length=120)
    def get_absolute_url(self):
        return "/group/%i/" % self.id
    def get_safety_code_url(self):
        return "/group/%i/safety_code/" % self.id

class Course(models.Model):
    name = models.CharField(max_length=254)
    report_type = models.CharField(max_length=254)
    teacher_name = models.CharField(max_length=254)
    beginning_date = models.DateField()
    ending_date = models.DateField()
    subject = models.ForeignKey(Subject)
    model_groups = models.ManyToManyField(ModelGroup)
    groups_allowed = models.ManyToManyField(Group)
    users_allowed = models.ManyToManyField(UserProfile)
    subject = models.ForeignKey('Subject')
    def get_absolute_url(self):
        return "/course/%i/" % self.id

class CommonMaterial(models.Model):
    text = models.TextField()
    subject = models.ForeignKey('Subject')

class Class(models.Model):
    conspect = models.TextField()
    homework = models.TextField()
    data = models.DateTimeField()
    is_canceled = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class ClassFormat(models.Model):
    day_of_week = models.IntegerField()
    type_of_class = models.CharField(max_length=254)
    time_of_beginning = models.TimeField()
    time_of_ending = models.TimeField()
    building = models.CharField(max_length=30)
    auditorium = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_number = models.IntegerField()

class ClassMaterial(models.Model):
    text = models.TextField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

class SecretCode(models.Model):
    code = models.CharField(max_length=8)

# def user_registered_callback(sender, user, request, **kwargs):
#     profile = UserProfile(user = user)

#     profile.is_lecturer = bool(request.POST["is_lecturer"])
#     profile.first_name = request.POST["first_name"]
#     profile.middle_name = request.POST["middle_name"]
#     profile.last_name = request.POST["last_name"]
#     profile.phone_number = request.POST["phone_number"]
#     profile.email = request.POST["email"]
#     profile.degree = request.POST["degree"]

#     group = Group(number = "100/1")
#     group.starosta_id = profile
#     group.save()

#     profile.save()

# user_registered.connect(user_registered_callback)

# @receiver(post_save, sender=Course)
# def post_save_course_ds(sender,instance, **kwargs):
#     if (use)
#     instance.faculty

class EmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        logger.error('Something wrong in authentificate!')

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None