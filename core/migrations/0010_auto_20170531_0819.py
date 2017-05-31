# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 08:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_userprofile_group_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='group_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Group'),
        ),
    ]
