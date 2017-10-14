# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from api  import permissions
from api.models import * 
from api.serializers import *

from rest_framework.permissions import *
from rest_framework.decorators import api_view,parser_classes,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework_jwt import authentication
import requests
import json
import os


APPID="wx792afb48d3249315"
APPSECRET="8145f1c123ddef11dd514f69314e7032"

#搜索手册和公司
@api_view(['POST'])
@permission_classes((AllowAny, ))
def search(request,format=None):
	companys=[]
	manuals=[]
	print request.data
	key=request.data["key"]
	manualResult= Manual.objects.filter(title__icontains=key)
	companyResult = Company.objects.filter(companyName__icontains=key)
	for company in companyResult:
		serializer=CompanySerializer(company,context={'request':request})
		companys.append(serializer.data)

	for manual in manualResult:
		serializer= ManualSerializer(manual,context={'request': request})
		manuals.append(serializer.data)
	return JsonResponse({"companys":companys,"manuals":manuals})

# 获取JWT之后需要获取自己公司信息
@api_view(['GET'])
@permission_classes((AllowAny, ))
def getuser(request,format=None):
	print request.user.id
	company=Company.objects.get(id=request.user.id)
	serializer=CompanySerializer(company,context={'request':request})
	print type(serializer.data)
	return Response(serializer.data)

#图片上传
@api_view(['POST'])
@permission_classes((AllowAny, ))
def upload(request,format=None):
	print request.data

	# 公司logo
	if request.data.has_key('logo'):
		logo=request.data["logo"]
		id=request.data["url"].split('/')[-2]
		company=Company.objects.get(id=id)
		company.logo=logo
		company.save()
		serializer=CompanySerializer(company,context={'request':request})

	# 产品图片
	elif request.data.has_key('productImage'):
		productImage=request.data["productImage"]
		id=request.data["url"].split('/')[-2]
		manual=Manual.objects.get(id=id)
		manual.image=productImage
		manual.save()
		serializer=ManualSerializer(manual,context={'request':request})
	# 视频	
	elif request.data.has_key('video'):
		video=request.data["video"]
		id=request.data["url"].split('/')[-2]
		manual=Manual.objects.get(id=id)
		manual.video=video
		manual.save()
		serializer=ManualSerializer(manual,context={'request':request})

	# 视频	
	elif request.data.has_key('docImages'):
		image=request.data["docImages"]
		id=request.data["url"].split('/')[-2]
		manual=Manual.objects.get(id=id)
		docImage=DocImage(manual=manual,image=image)
		docImage.save()
		
		serializer=ManualSerializer(manual,context={'request':request})
	return Response(serializer.data)


# 生成当前页面的二维码
@api_view(['GET'])
@permission_classes((AllowAny,))
def getqrcode(request,format=None):
	url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+APPSECRET
	access_token = requests.get(url).json()["access_token"]
	print access_token
	url2="https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode?access_token="+access_token
	qrcode=requests.post(url2,data=json.dumps({"path": "pages/index/index", "width": 430})).json()
	with open('media／qrcode／picture.jpg', 'wb') as file:
		file.write(qrcode.content)
	return JsonResponse(qrcode)



## list／create／retrieve／update／partial_update／destroy

class CompanyViewSet(viewsets.ModelViewSet):
	"""
	-- create：AllowAny
	-- delete list：IsAdminUser
	-- others：AllowAny
	"""
	queryset = Company.objects.all()
	serializer_class = CompanySerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {"retrieve":[AllowAny,],"create":[AllowAny,]}

	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class ManualViewSet(viewsets.ModelViewSet):
	"""
	-- create：AllowAny
	-- delete list：IsAdminUser
	-- others：AllowAny
	"""
	queryset = Manual.objects.all()
	serializer_class = ManualSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {"retrieve":[AllowAny,]}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class DocImageViewSet(viewsets.ModelViewSet):
	"""
	-- create：AllowAny
	-- delete list：IsAdminUser
	-- others：AllowAny
	"""
	queryset = DocImage.objects.all()
	serializer_class = DocImageSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {"retrieve":[AllowAny,]}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]