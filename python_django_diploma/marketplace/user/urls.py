from django.urls import path

from user.views import (
    UserRegistrationAPIView, UserLogoutAPIView, ProfileAPIView,
    ProfileAvatarAPIView, ProfilePasswordAPIView, UserLoginAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


urlpatterns = [
    path('sign-up/', UserRegistrationAPIView.as_view(), name='sign-up'),
    path('sign-in/', UserLoginAPIView.as_view(), name='sign-in'),
    path('sign-out/', UserLogoutAPIView.as_view(), name='sign-out'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/avatar/', ProfileAvatarAPIView.as_view(), name='profile-avatar'),
    path('profile/password/', ProfilePasswordAPIView.as_view(), name='profile-password'),
]
