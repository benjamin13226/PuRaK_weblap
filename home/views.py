# Import HttpResponseRedirect and redirect helpers for language switching
from django.shortcuts import redirect


def switch_language(request, lang_code):
    # Validate language code input
    if lang_code not in ['hu', 'en']:
        lang_code = 'hu'
    
    # Retrieve HTTP referrer URL or default to root home page
    next_url = request.META.get('HTTP_REFERER', '/')
    
    # Prepare redirect response and store selected language in cookie
    response = redirect(next_url)
    response.set_cookie('site_language', lang_code, max_age=365*24*60*60)
    return response