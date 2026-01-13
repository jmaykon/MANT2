from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # login raíz
    path('', include(('apps.users.urls', 'users'), namespace='users')),

    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('mantenimiento/', include(('apps.mantenimiento.urls', 'mantenimiento'), namespace='mantenimiento')),
    path('equipo/', include(('apps.equipo.urls', 'equipo'), namespace='equipo')),
    path('lugar/', include(('apps.lugar.urls', 'lugar'), namespace='lugar')),
]

# ✅ Habilita archivos de MEDIA (firmas, imágenes, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
