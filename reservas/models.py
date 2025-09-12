from django.db import models
from django.conf import settings


class Booking(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    class_session = models.ForeignKey(
        "academia.ClassSession",
        on_delete=models.PROTECT,
        related_name="bookings"
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    calendar_event_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status", "created_at"]),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.user} - {self.class_session} ({self.status})"
    

    # Actualiza la capacidad al crear una reserva
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.class_session.capacity > 0:
            self.class_session.capacity -= 1
            self.class_session.save()

            # Sincroniza con Google Calendar si el usuario es PREMIUM
            from reservas.services import create_google_calendar_event
            event_id = create_google_calendar_event(self.user, self.class_session, self)
            if event_id:
                self.calendar_event_id = event_id
                super().save(update_fields=['calendar_event_id'])

