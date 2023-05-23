import debug_toolbar
from django.conf import settings
from django.conf.urls.static import serve
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
urlpatterns = [
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path("", include("core.urls")),
    path("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path("", include("core.routes")),
    path("users/", include("users.urls")),
    re_path("^docs/(?P<path>.*)$", serve, {"document_root": settings.DOCS_ROOT}),
]

urlpatterns += [
    path("__debug__/", include(debug_toolbar.urls)),
]
