# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-25 00:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('companyName', models.CharField(max_length=40, null=True)),
                ('brief', models.CharField(blank=True, max_length=500)),
                ('logo', models.ImageField(max_length=256, null=True, upload_to='logo')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='image')),
                ('document', models.FileField(null=True, upload_to='doc')),
                ('video', models.FileField(null=True, upload_to='video')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
