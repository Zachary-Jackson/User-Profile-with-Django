# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-16 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171216_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default=None),
        ),
    ]
