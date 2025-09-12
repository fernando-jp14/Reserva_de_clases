from django.urls import path
from .views import UserRegisterView
from .views_google import google_calendar_auth, google_calendar_callback, google_calendar_token_save

urlpatterns = [
	path('register/', UserRegisterView.as_view(), name='user-register'),
    path('google-calendar/auth/', google_calendar_auth, name='google-calendar-auth'),
    path('oauth2callback/', google_calendar_callback, name='google-calendar-callback'),
    path('google-calendar/token/', google_calendar_token_save, name='google-calendar-token-save'),
]
