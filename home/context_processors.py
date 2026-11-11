# Import navigation and footer models to inject localized variables globally
from home.models import MenuItem, FooterSettings


def menu_context(request):
    # Retrieve current active language from cookie (defaults to 'hu')
    current_lang = request.COOKIES.get('site_language', 'hu')
    
    # Fetch root navigation items ordered by sort_order
    top_menu_items = MenuItem.objects.filter(parent__isnull=True).order_by('sort_order')
    
    # Retrieve active footer settings snippet
    footer_settings = FooterSettings.objects.first()
    
    return {
        'menu_items': top_menu_items,
        'footer_settings': footer_settings,
        'current_lang': current_lang,
    }