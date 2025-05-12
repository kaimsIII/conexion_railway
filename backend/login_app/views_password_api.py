from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, status, views, permissions
from rest_framework.response import Response

from .serializers import (
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)

User = get_user_model()


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        if not User.objects.filter(email=email).exists():
            return Response({"detail": "Si el correo está registrado, se enviará un enlace de recuperación."},
                            status=status.HTTP_200_OK)

        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        domain = get_current_site(request).domain
        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        absurl = f"http://{domain}{relative_link}"

        email_body = f'Hola, usa este enlace para cambiar tu contraseña:\n\n{absurl}'
        email_subject = 'Recuperación de contraseña'

        email_message = EmailMessage(subject=email_subject, body=email_body, to=[email])
        email_message.send()

        return Response({'detail': 'Enlace de recuperación enviado.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(views.APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'detail': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
