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
	instructor_id = serializers.IntegerField(source='instructor.id', read_only=True)
	instructor_name = serializers.CharField(source='instructor.first_name', read_only=True)
	class_type_id = serializers.IntegerField(source='class_type.id', read_only=True)
	class_type_name = serializers.CharField(source='class_type.name', read_only=True)

	class Meta:
		model = ClassSession
		fields = [
			'id',
			'title',
			'start',
			'end',
			'capacity',
			'instructor_id',
			'instructor_name',
			'class_type_id',
			'class_type_name',
		]
