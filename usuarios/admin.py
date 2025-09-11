from django.contrib import admin
from .models import User, Membership

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'membership')
    list_filter = ('membership',)
    search_fields = ('username', 'email')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_bookings_per_day', 'has_google_sync')
