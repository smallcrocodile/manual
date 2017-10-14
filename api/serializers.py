from rest_framework import serializers
from api.models import *


# class SimpleCompanySerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = Company
# 		fields = ('url','id','companyName')

class DocImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DocImage
		fields = '__all__'
		

class ManualSerializer(serializers.HyperlinkedModelSerializer):
	docImages= DocImageSerializer(read_only=True,many=True)
	class Meta:
		model = Manual
		fields = '__all__'


class CompanySerializer(serializers.HyperlinkedModelSerializer):
	manual = ManualSerializer(many=True,read_only=True)
	class Meta:
		model = Company
		fields='__all__'
		# exclude = ('is_admin','is_active') 

	def create(self, validated_data):
		user = Company(name=validated_data["name"],companyName=validated_data["companyName"],brief=validated_data["brief"])
		user.set_password(validated_data["password"])
		user.save()
		return user