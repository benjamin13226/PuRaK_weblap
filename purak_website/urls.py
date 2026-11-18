# Import Django URL routing modules and Wagtail core configurations
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views
from home.views import switch_language

urlpatterns = [
    # Django administration route
    path("django-admin/", admin.site.urls),
    # Wagtail administration interface route
    path("admin/", include(wagtailadmin_urls)),
    # Wagtail document serving route
    path("documents/", include(wagtaildocs_urls)),
    # Site search view route
    path("search/", search_views.search, name="search"),
    # Cookie-based language switching endpoint
    path("set-language/<str:lang_code>/", switch_language, name="set_language"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and uploaded media files during local development
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # Wagtail page serving fallback route
    path("", include(wagtail_urls)),
]