from django.contrib import admin
from .models import ClassType, Instructor, ClassSession

@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'active')
	search_fields = ('name',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email', 'active')
	search_fields = ('first_name', 'last_name', 'email')
	list_filter = ('active', 'specialty')

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
	list_display = ('title', 'instructor', 'class_type', 'start', 'end', 'capacity', 'available_slots')
	search_fields = ('title',)
	list_filter = ('class_type', 'instructor')
