from django.urls import path, include
from . import views
from views_s import home

urlpatterns = [
    path('', home.home, name='home'),
    path('documentation/', home.documentation, name='documentation'),
    path('community/', home.community, name='community'),
    path('collection/', views.collection, name='collection'),
    path('exhibit_select/', views.exhibit_select, name='exhibit_select'),
    path('exhibit/', views.exhibit_detail, name="exhibit-detail"),
    path('artwork/', views.artwork_preview, name="artwork-preview"),
    path('generator/', home.marker_generator, name='marker-generator'),
    path('sw.js', views.service_worker, name='sw'),
    path('manifest.json', views.manifest, name='manifest'),
    path('upload', views.upload_image, name='upload-image'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('see_all/', views.see_all, name='see-all'),
    path('robots.txt/', views.robots_txt),
]
