from django.db import models
from django.contrib.auth.models import AbstractUser

class Membership(models.Model):
    """
    Membership: FREE / PREMIUM
    """
    name = models.CharField(max_length=32, unique=True)  # e.g. "FREE", "PREMIUM"
    max_bookings_per_day = models.PositiveIntegerField(null=False)
    has_google_sync = models.BooleanField(default=False)

    class Meta:
        db_table = "membresia"
        verbose_name = "membresia"
        verbose_name_plural = "membresias"

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    """
    Custom user based on AbstractUser.
    Has a FK to Membership.
    """
    membership = models.ForeignKey(
        Membership,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
        help_text="Membresía asignada a la usuario (e.g. FREE, PREMIUM)."
    )

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.get_username()


class GoogleCalendarToken(models.Model):
    user = models.OneToOneField(
        'usuarios.User',
        on_delete=models.CASCADE,
        related_name='google_calendar_token'
    )
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Calendar Token for {self.user.username}"

