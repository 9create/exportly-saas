from .models import PlatformSettings
from inquiries.models import Inquiry # Naya import

def platform_colors(request):
    settings = PlatformSettings.load()
    
    # Default count 0 rakho
    unread_count = 0
    
    # Agar user login hai, toh uske unread messages count karo
    if request.user.is_authenticated:
        unread_count = Inquiry.objects.filter(exporter=request.user, is_read=False).count()
        
    return {
        'site_settings': settings,
        'global_unread_inquiries': unread_count # Sidebar ke liye
    }