from django.contrib import admin
from django.urls import path
from accounts.views import UserProfileView
from accounts.views import register_user

# Import the built-in JWT Views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Endpoint to exchange username/password for an access token (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 2. Endpoint to automatically renew expired tokens behind the scenes
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Your user profile data endpoint
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    path('api/register/', register_user, name='register'),
]