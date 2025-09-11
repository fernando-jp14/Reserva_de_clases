from rest_framework import serializers
from .models import ClassType, Instructor, ClassSession

class ClassTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClassType
		fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instructor
		fields = '__all__'

class ClassSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClassSession
		fields = '__all__'
