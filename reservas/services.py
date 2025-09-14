from .models import Booking
from django.utils import timezone
# Función para crear un evento en Google Calendar para usuarios PREMIUM
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from usuarios.models import GoogleCalendarToken

def create_booking_and_update_capacity(user, class_session, **kwargs):
    # Solo permite reservar si hay capacidad
    if class_session.capacity <= 0:
        raise ValueError("No hay cupos disponibles para esta clase.")

    # Validación de reservas diarias según membresía (rango de fechas para todo el día)
    from datetime import datetime, time
    fecha_reserva = class_session.start.date()
    fecha_inicio = datetime.combine(fecha_reserva, time.min)
    fecha_fin = datetime.combine(fecha_reserva, time.max)
    reservas_hoy = Booking.objects.filter(
        user=user,
        status=Booking.STATUS_ACTIVE,
        class_session__start__gte=fecha_inicio,
        class_session__start__lte=fecha_fin
    ).count()
    membresia = getattr(user, 'membership', None)
    max_por_dia = membresia.max_bookings_per_day if membresia else 1
    if reservas_hoy >= max_por_dia:
        raise ValueError("No puedes reservar más clases para este día según tu membresía.")

    booking = Booking.objects.create(user=user, class_session=class_session, **kwargs)
    return booking

def create_google_calendar_event(user, class_session, booking):
    """
    Crea un evento en Google Calendar para el usuario PREMIUM cuando se crea una reserva.
    - user: instancia de User
    - class_session: instancia de ClassSession
    - booking: instancia de Booking
    """
    # Verificar membresía y token
    membership = getattr(user, 'membership', None)
    if not (membership and getattr(membership, 'name', '').upper() == 'PREMIUN'):
        return None  # Solo usuarios PREMIUM
    try:
        token_obj = user.google_calendar_token
    except GoogleCalendarToken.DoesNotExist:
        return None  # No tiene token

    # Crear credenciales de Google
    creds = Credentials(
        token=token_obj.access_token,
        refresh_token=token_obj.refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=None,  # Se puede omitir si solo usas el token
        client_secret=None,
        scopes=['https://www.googleapis.com/auth/calendar.events']
    )
    service = build('calendar', 'v3', credentials=creds)

    # Preparar datos del evento
    event = {
        'summary': class_session.title,
        'description': f'Reserva: {booking.id} | Usuario: {user.username}',
        'start': {
            'dateTime': class_session.start.isoformat(),
            'timeZone': 'America/Lima',
        },
        'end': {
            'dateTime': class_session.end.isoformat(),
            'timeZone': 'America/Lima',
        },
    }
    # Crear el evento en el calendario principal
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    # Opcional: puedes guardar el event_id en el modelo Booking si lo necesitas
    return created_event.get('id')
