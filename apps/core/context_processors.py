from .models import SiteConfig


def site_settings(request):
    return {
        'site_config': SiteConfig.get_solo(),
    }
