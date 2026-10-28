from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Admin panel ki list me ye fields dikhenge
    list_display = ('username', 'email', 'company_name', 'iec_code', 'is_staff')
    
    # Jab kisi user ko edit karne jayenge, toh ye naye fields dikhenge
    fieldsets = UserAdmin.fieldsets + (
        ('Exporter Details', {'fields': ('company_name', 'iec_code', 'phone', 'is_exporter')}),
    )

admin.site.register(User, CustomUserAdmin)