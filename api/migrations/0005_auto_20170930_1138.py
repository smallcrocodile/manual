# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-30 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170926_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='brief',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]