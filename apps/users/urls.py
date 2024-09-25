from django.urls import path

from . import views
from .sso_login import sso_redirect, after_login_redirect
from .views import sso_login_view


app_name = "users"
urlpatterns = [
    path("profile/", views.profile, name="user_profile"),
    path("profile/upload-image/", views.upload_profile_image, name="upload_profile_image"),
    path('sso/login/', sso_login_view, name='sso_login'),
    path('sso/redirect/', after_login_redirect, name='after_login_redirect'),
]
