from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SitePage, PricingPlan, PromoCode, PlatformSettings

class CustomUserAdmin(UserAdmin):
    # Admin panel ki list me ye fields dikhenge
    list_display = ('username', 'email', 'company_name', 'iec_code', 'is_staff')
    
    # Jab kisi user ko edit karne jayenge, toh ye naye fields dikhenge
    # Yahan humne 'Subscription Info' wala naya section add kiya hai
    fieldsets = UserAdmin.fieldsets + (
        ('Exporter Details', {'fields': ('company_name', 'iec_code', 'phone','whatsapp_number', 'is_exporter', 'template_choice')}),
        ('Subscription Info', {'fields': ('current_plan', 'trial_ends_at')}), 
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(PricingPlan)
admin.site.register(PromoCode)


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Sirf ek hi settings ban sake
        return not PlatformSettings.objects.exists()