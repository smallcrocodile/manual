# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class MyUserManager(BaseUserManager):
	def create_user(self,name, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not name:
			raise ValueError('Users must have an name')

		user = self.model(
			name=name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,name, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			name=name,
			password=password
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class Company(AbstractBaseUser):
	name = models.CharField(max_length=20,unique=True)
	companyName=models.CharField(max_length=40,unique=True,blank=True)
	brief= models.CharField(max_length=500,blank=True)
	logo=models.ImageField(upload_to='logo', max_length=256,blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()
	USERNAME_FIELD = 'name'
	#REQUIRED_FIELDS = ['name',]
	def get_full_name(self):
		# The user is identified by their email address
		return self.name

	def get_short_name(self):
		# The user is identified by their email address
		return self.name

	def __str__(self):
	# __unicode__ on Python 2
		return self.name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	def __unicode__(self):
		return self.name

class Manual(models.Model):
	company=models.ForeignKey(Company,related_name="manual")
	title=models.CharField(max_length=120)
	content=models.CharField(max_length=500,blank=True)
	qrcode=models.ImageField(upload_to='qrcode',blank=True)
	image = models.ImageField(upload_to='image',blank=True)
	document=models.FileField(upload_to='doc', blank=True)
	video=models.FileField(upload_to='video', blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

class DocImage(models.Model):
	manual=models.ForeignKey(Manual,related_name="docImages")
	image = models.ImageField(upload_to='docImages',blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
		



