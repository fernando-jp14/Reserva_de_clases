from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import ClassType, Instructor, ClassSession
from .serializers import ClassTypeSerializer, InstructorSerializer, ClassSessionSerializer

class ClassTypeViewSet(viewsets.ModelViewSet):
	#permission_classes = [IsAuthenticated]
	queryset = ClassType.objects.all()
	serializer_class = ClassTypeSerializer

class InstructorViewSet(viewsets.ModelViewSet):
	queryset = Instructor.objects.all()
	serializer_class = InstructorSerializer

class ClassSessionViewSet(viewsets.ModelViewSet):
	queryset = ClassSession.objects.all()
	serializer_class = ClassSessionSerializer
