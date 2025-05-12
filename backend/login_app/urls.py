from django.urls import path
from .views_api import LoginAPIView, RegisterAPIView, LogoutAPIView, GoogleLoginAPIView
from .views_password_api import RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Rutas API REST
    path('api/auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Recuperación de contraseña
    path('api/auth/request-reset-password/', RequestPasswordResetEmail.as_view(), name='request-reset-password'),
    path('api/auth/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('api/auth/set-new-password/', SetNewPasswordAPIView.as_view(), name='set-new-password'),

    # Login con Google
    path('api/auth/google/', GoogleLoginAPIView.as_view(), name='google_login'),

]
