from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CurrentUserView,
    UserProfileAPIView
)

urlpatterns = [
    # Аутентификация
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Пользователь
    path('me/', CurrentUserView.as_view(), name='api_current_user'),
    path('profile/', UserProfileAPIView.as_view(), name='api_user_profile'),
]