from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from .services import create_booking_and_update_capacity

class BookingViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer

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
