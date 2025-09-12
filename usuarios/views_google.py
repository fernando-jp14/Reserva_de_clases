from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
from .models import GoogleCalendarToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse

# Vista para iniciar la autorización de Google Calendar
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_calendar_auth(request):
    # Solo usuarios PREMIUM
    membership = getattr(request.user, 'membership', None)
    if not (membership and getattr(membership, 'name', '').upper() == 'PREMIUN'):
        return Response({'detail': 'Solo usuarios PREMIUM pueden vincular Google Calendar.'}, status=403)

    creds_path = os.path.join(settings.BASE_DIR, 'credenciales', 'client_secret.json')
    flow = Flow.from_client_secrets_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/calendar.events'],
        redirect_uri='http://localhost:8000/api/usuarios/oauth2callback/'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['google_auth_state'] = state
    return Response({'authorization_url': authorization_url})

#@login_required
def google_calendar_callback(request):
    state = request.session.get('google_auth_state')
    code = request.GET.get('code')
    if not code:
        return HttpResponse('No se recibió el código de autorización.', status=400)

    creds_path = os.path.join(settings.BASE_DIR, 'credenciales', 'client_secret.json')
    flow = Flow.from_client_secrets_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/calendar.events'],
        redirect_uri='http://localhost:8000/api/usuarios/oauth2callback/',
        state=state
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Mostrar los tokens en pantalla para copiar
    html = f"""
    <h2>Token de Google Calendar generado</h2>
    <p><b>access_token:</b> {credentials.token}</p>
    <p><b>refresh_token:</b> {getattr(credentials, 'refresh_token', '')}</p>
    <p><b>token_expiry:</b> {getattr(credentials, 'expiry', '')}</p>
    <p>Copia estos valores y envíalos al endpoint <code>/api/usuarios/google-calendar/token/</code> usando tu JWT.</p>
    """
    return HttpResponse(html)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def google_calendar_token_save(request):
    """
    Endpoint para guardar el token de Google Calendar desde el frontend o manualmente.
    Recibe: access_token, refresh_token, token_expiry
    """
    access_token = request.data.get('access_token')
    refresh_token = request.data.get('refresh_token')
    token_expiry = request.data.get('token_expiry')
    if not access_token:
        return Response({'detail': 'Falta access_token.'}, status=400)
    GoogleCalendarToken.objects.update_or_create(
        user=request.user,
        defaults={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expiry': token_expiry
        }
    )
    return Response({'detail': 'Token guardado correctamente.'})
