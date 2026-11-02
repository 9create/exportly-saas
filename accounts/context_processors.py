from .models import PlatformSettings

def platform_colors(request):
    # Database se settings load karo
    settings = PlatformSettings.load()
    return {
        'site_settings': settings
    }