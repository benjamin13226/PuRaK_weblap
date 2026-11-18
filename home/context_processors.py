# Import navigation, footer, and news models to inject localized context globally
from home.models import MenuItem, FooterSettings, NewsPost


def menu_context(request):
    # Retrieve active language code from cookie
    current_lang = request.COOKIES.get("site_language", "hu")

    # Fetch top-level menu items sorted by sort_order
    top_menu_items = MenuItem.objects.filter(parent__isnull=True).order_by("sort_order")

    # Retrieve footer and top bar settings snippet
    footer_settings = FooterSettings.objects.first()

    # Retrieve published news posts ordered by pinned status and publication date
    news_posts = NewsPost.objects.filter(is_published=True).prefetch_related("subpage_links__target_page")

    return {
        "menu_items": top_menu_items,
        "footer_settings": footer_settings,
        "news_posts": news_posts,
        "current_lang": current_lang,
    }