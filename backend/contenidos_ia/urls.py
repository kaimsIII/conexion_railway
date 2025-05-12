from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API de Autenticación",
        default_version='v1',
        description="Documentación de la API REST de Login, Registro y Recuperación de Contraseña",
        contact=openapi.Contact(email="soporte@tuempresa.com"),
        license=openapi.License(name="MIT"),
    ),

    #Para desarrollo   
    # public=False,  # importante para mantenerlo privado
    # permission_classes=[permissions.IsAdminUser],  # solo admins pueden acceder

    public=True,
    permission_classes= [],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login_app.urls')),  # Incluye las URLs de login_app
    path('accounts/', include('allauth.urls')), # login externo
        
    # Rutas para la recuperación de contraseña
    path('restore/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('restore/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    # Redirige a la documentación de la API por defecto
    path('', RedirectView.as_view(url='docs/', permanent=False)),

    #swagger y redoc
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)