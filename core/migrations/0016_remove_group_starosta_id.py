# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 09:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_group_starosta_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='starosta_id',
        ),
    ]