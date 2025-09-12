
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, BasePermission
from rest_framework import viewsets
from .models import ClassType, Instructor, ClassSession
from .serializers import ClassTypeSerializer, InstructorSerializer, ClassSessionSerializer

# Permiso personalizado: solo superusuario puede modificar, todos los autenticados pueden ver
class IsSuperUserOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return request.user and request.user.is_authenticated
		return request.user and request.user.is_superuser

class ClassTypeViewSet(viewsets.ModelViewSet):
	queryset = ClassType.objects.all()
	serializer_class = ClassTypeSerializer
	permission_classes = [IsSuperUserOrReadOnly]

class InstructorViewSet(viewsets.ModelViewSet):
	queryset = Instructor.objects.all()
	serializer_class = InstructorSerializer
	permission_classes = [IsSuperUserOrReadOnly]

class ClassSessionViewSet(viewsets.ModelViewSet):
	queryset = ClassSession.objects.all()
	serializer_class = ClassSessionSerializer
	permission_classes = [IsSuperUserOrReadOnly]
