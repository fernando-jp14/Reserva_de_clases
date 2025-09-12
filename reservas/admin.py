from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'class_session', 'status', 'created_at', 'updated_at')
	list_filter = ('status', 'user', 'class_session')
	search_fields = ('user__username', 'class_session__title')
	#Con esto, los campos aparecerán en el formulario de edición como solo lectura.
	readonly_fields = ('created_at', 'updated_at')
