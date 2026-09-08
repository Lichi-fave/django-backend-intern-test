from django.contrib import admin
from .models import Department, Employee

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'department', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['department', 'is_active']


