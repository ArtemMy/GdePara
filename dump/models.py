from django.db import models
from django.utils import timezone

class Data(models.Model):
    user = models.ForeignKey('auth.User')
    data = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title


class Course(models.Model):
    report_type = models.CharField(max_length=254)
    beginning_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    courses = models.ManyToManyField(User)
    courses = models.ManyToManyField(Group)

class Subject(models.Model):
    name = models.CharField(max_length=254)
    is_necessary = models.BooleanField(initial=False)

class CommonMaterial(models.Model):
    text = models.TextField()
    subjects = models.ManyToManyField(Subject)

class Class(models.Model):
    conspect = models.TextField()
    homework = models.TextField()
    data = models.DateTimeField()
    is_canceled = models.BooleanField(initial=False)
    group_id = models.ForeignKey(Course, on_delete=models.CASCADE)

class ClassFormat(models.Model):
    day_of_week = models.IntegerField()
    type_of_class = models.CharField(max_length=254)
    time_of_beginning = models.TimeField()
    time_of_ending = models.TimeField()
    building = models.CharField(max_length=30)
    auditorium = models.CharField(max_length=30)
    starosta_id = models.OneToOneField(Course, on_delete=models.CASCADE)
    week_number = models.IntegerField()

class CourseMaterial(models.Model):
    text = models.TextField()
    courses = models.ManyToManyField(Course)