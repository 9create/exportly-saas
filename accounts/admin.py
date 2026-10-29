from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SitePage, PricingPlan

class CustomUserAdmin(UserAdmin):
    # Admin panel ki list me ye fields dikhenge
    list_display = ('username', 'email', 'company_name', 'iec_code', 'is_staff')
    
    # Jab kisi user ko edit karne jayenge, toh ye naye fields dikhenge
    # Yahan humne 'Subscription Info' wala naya section add kiya hai
    fieldsets = UserAdmin.fieldsets + (
        ('Exporter Details', {'fields': ('company_name', 'iec_code', 'phone', 'is_exporter')}),
        ('Subscription Info', {'fields': ('current_plan', 'trial_ends_at')}), 
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(PricingPlan)