from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from .services import create_booking_and_update_capacity

from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permiso personalizado: solo superusuario y usuario PREMIUM pueden editar/eliminar su reserva
class IsSuperUserOrPremiumOwnerOrReadOnly(BasePermission):
	def has_object_permission(self, request, view, obj):
		# Métodos seguros: cualquiera autenticado puede ver
		if request.method in SAFE_METHODS:
			return request.user and request.user.is_authenticated
		# Superusuario puede modificar cualquier reserva
		if request.user.is_superuser:
			return True
		# Usuario PREMIUM puede modificar solo su propia reserva
		membership = getattr(request.user, 'membership', None)
		if membership and getattr(membership, 'name', '').upper() == 'PREMIUN':
			return obj.user == request.user
		return False

class BookingViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [IsSuperUserOrPremiumOwnerOrReadOnly]

	"""
	Permite personalizar el proceso de creación de una reserva.
	Valida los datos recibidos.
	Obtiene el usuario autenticado y la sesión de clase.
	Llama a la función create_booking_and_update_capacity para aplicar la lógica de negocio (verifica cupos, límites por membresía, etc.).
	Si ocurre un error (por ejemplo, no hay cupos o el usuario FREE ya reservó ese día), devuelve un mensaje de error personalizado.
	Si todo está bien, crea la reserva y devuelve los datos de la nueva reserva.
	"""
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = request.user
		class_session = serializer.validated_data['class_session']
		# Otros campos
		extra_fields = {k: v for k, v in serializer.validated_data.items() if k not in ['user', 'class_session']}
		try:
			booking = create_booking_and_update_capacity(user, class_session, **extra_fields)
		except ValueError as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		read_serializer = self.get_serializer(booking)
		return Response(read_serializer.data, status=status.HTTP_201_CREATED)
