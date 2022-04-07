from django.urls import path, include
from .views import get_artwork_preview, get_all_items, service_worker, upload_image_form, exhibit_select_form, get_collection_items, get_exhibit_detail, manifest, get_robots_txt
from .views_s.home import home, community, marker_generator, documentation

urlpatterns = [
    path('', home, name='home'),
    path('documentation/', documentation, name='documentation'),
    path('community/', community, name='community'),
    path('collection/', get_collection_items, name='get_collection_items'),
    path('exhibit_select/', exhibit_select_form, name='exhibit_select_form'),
    path('exhibit/', get_exhibit_detail, name="get_exhibit_detail"),
    path('artwork/', get_artwork_preview, name="get_artwork_preview"),
    path('generator/', marker_generator, name='marker_generator'),
    path('sw.js', service_worker, name='sw'),
    path('manifest.json', manifest, name='manifest'),
    path('upload', upload_image_form, name='upload_image_form'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('see_all/', get_all_items, name='get_all_items'),
    path('robots.txt/', get_robots_txt),
]
