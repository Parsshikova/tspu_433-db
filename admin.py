from django.contrib import admin
from .models import Faculty, Group, Student

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'course')
    list_filter = ('faculty', 'course')
    search_fields = ('name', 'faculty__name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'group', 'is_active')
    list_filter = ('group', 'is_active', 'gender')
    search_fields = ('last_name', 'first_name', 'middle_name', 'email')
    raw_id_fields = ('group',)
