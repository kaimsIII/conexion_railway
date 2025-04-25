from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Campo adicional que quieres mantener
    nombre_completo = models.CharField(max_length=100, blank=True)

    # Eliminamos first_name y last_name explícitamente si no los quieres
    first_name = None
    last_name = None

    # Sobrescribimos las relaciones para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Nombre único para el accessor inverso
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Nombre único para el accessor inverso
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Opcional: Define los campos que quieres que se muestren en el admin o en otros contextos
    class Meta:
        db_table = 'login_app_customuser'  # Asegúrate de que coincida con tu tabla actual
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username