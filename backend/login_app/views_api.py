from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    LogoutSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
import requests
from allauth.socialaccount.models import SocialApp
from rest_framework import serializers

User = get_user_model()


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=GoogleAuthSerializer)
    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "Token de Google no proporcionado."}, status=400)

        # Obtener el client_id registrado en Django admin para validar contra Google
        try:
            google_app = SocialApp.objects.get(provider="google")
            expected_audience = google_app.client_id
        except SocialApp.DoesNotExist:
            return Response({"error": "Configuración de Google no encontrada en el backend."}, status=500)

        # Validar el token con Google
        google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        response = requests.get(google_url)
        if response.status_code != 200:
            return Response({"error": "Token de Google inválido."}, status=400)

        data = response.json()
        email = data.get("email")
        name = data.get("name")
        aud = data.get("aud")

        if aud != expected_audience:
            return Response({"error": "El token no coincide con el client_id configurado."}, status=403)

        if not email:
            return Response({"error": "No se pudo obtener el correo del token."}, status=400)

        username = email.split("@")[0]
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": username,
            "nombre_completo": name,
        })

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request)
        return Response({'detail': 'Enlace de recuperación enviado.'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=SetNewPasswordSerializer)
    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)