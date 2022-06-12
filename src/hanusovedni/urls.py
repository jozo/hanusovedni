from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from home import views

handler404 = views.handler404

urlpatterns = [
    path("admin/django/", admin.site.urls),
    path("admin/autocomplete/", include(autocomplete_admin_urls)),
    path("admin/i18n/", include("django.conf.urls.i18n")),
    path(
        "admin/choose-lang/<str:lang_code>/", views.choose_language, name="choose-lang"
    ),
    path("admin/", include(wagtailadmin_urls)),
    re_path(r"^recnici/(.*)/$", views.redirect_speakers),
    re_path(r"^archiv/(.*)/$", views.redirect_events),
    re_path(r"^program/(.*)/$", views.redirect_events),
    path("api/stream/", views.stream_api, name="api-stream"),
    path("api/archive/", views.archive_api, name="api-archive"),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

urlpatterns += i18n_patterns(
    # These URLs will have /<language_code>/ appended to the beginning
    # url(r"^search/$", search_views.search, name="search"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r"^events/(\d+)/(.*)/$", views.redirect_wagtail_events),
    re_path(r"^speakers/(.*)/$", views.redirect_wagtail_speakers),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
