from .models import Booking
from django.utils import timezone

def create_booking_and_update_capacity(user, class_session, **kwargs):
	# Solo permite reservar si hay capacidad
	if class_session.capacity <= 0:
		raise ValueError("No hay cupos disponibles para esta clase.")

	# Validación de reservas diarias según membresía
	fecha_reserva = class_session.start.date()
	reservas_hoy = Booking.objects.filter(
		user=user,
		status=Booking.STATUS_ACTIVE,
		class_session__start__date=fecha_reserva
	).count()
	membresia = getattr(user, 'membership', None)
	max_por_dia = membresia.max_bookings_per_day if membresia else 1
	if reservas_hoy >= max_por_dia:
		raise ValueError("No puedes reservar más clases para este día según tu membresía.")

	booking = Booking.objects.create(user=user, class_session=class_session, **kwargs)
	return booking
