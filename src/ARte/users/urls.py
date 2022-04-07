from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.jinja2',
        authentication_form=LoginForm,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('recover/', views.recover_password, name='recover'),
    path('recover-code/', views.recover_code, name='recover-code'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name="edit-profile"),
    path('profile/edit-password/', views.edit_password, name="edit-password"),
    path('wrong-verification-code', views.wrong_verification_code, name="wrong-verification-code"),
    path('invalid-recovering-email', views.invalid_recovering_email_or_username, name="invalid_recovering_email_or_username"),
    path('recover-edit-password', views.recover_edit_password, name="recover-edit-password"),

    path('markers/upload/', views.marker_upload, name='marker-upload'),
    path('objects/upload/', views.object_upload, name='object-upload'),
    path('element/get/', views.element_get, name='element-get'),

    path('objects/edit/', views.edit_object, name='edit-object'),
    path('markers/edit/', views.edit_marker, name='edit-marker'),

    path('artworks/create/', views.create_artwork, name='create-artwork'),
    path('artworks/edit/', views.edit_artwork, name="edit-artwork"),

    path('exhibits/create/', views.create_exhibit, name='create-exhibit'),
    path('exhibits/edit/', views.edit_exhibit, name='edit-exhibit'),
    path('download-exhibit', views.download_exhibit, name="download-exhibit"),

    path('content/delete/', views.delete, name='delete-content'),
    path('moderator-page/', views.mod, name='moderator-page'),
    path('permission-denied/', views.permission_denied, name='permission-denied'),
    path('content/mod-delete/', views.mod_delete, name='mod-delete-content'),
    path('related-content', views.related_content, name='related-content'),
]
