# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_course_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='beginning_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='ending_date',
            field=models.DateField(),
        ),
    ]
