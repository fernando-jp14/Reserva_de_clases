from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Membership, GoogleCalendarToken

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    #para agregar el campo membership en el admin de User
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('membership',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('membership',)}),
    )
    list_display = ('username', 'email', 'membership')
    list_filter = ('membership',)
    search_fields = ('username', 'email')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_bookings_per_day', 'has_google_sync')

@admin.register(GoogleCalendarToken)
class GoogleCalendarTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'token_expiry', 'created_at', 'updated_at')
    search_fields = ('user__username',)
