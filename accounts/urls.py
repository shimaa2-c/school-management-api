from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    LogoutView,
    MeView,
    ChangePasswordView,
)


urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register',
    ),

    path(
        'token/',
        CustomTokenObtainPairView.as_view(),
        name='token',
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),

    path(
        'me/',
        MeView.as_view(),
        name='me',
    ),

    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name='change_password',
    ),
]