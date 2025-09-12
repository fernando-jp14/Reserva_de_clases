from .models import Booking

def create_booking_and_update_capacity(user, class_session, **kwargs):
	# Solo permite reservar si hay capacidad
	if class_session.capacity <= 0:
		raise ValueError("No hay cupos disponibles para esta clase.")

	booking = Booking.objects.create(user=user, class_session=class_session, **kwargs)
	return booking
