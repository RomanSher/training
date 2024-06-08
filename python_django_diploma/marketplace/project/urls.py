from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from project.views import TestCeleryView


urlpatterns = [
    path('celery/', TestCeleryView.as_view(), name='celery_test'),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('user.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('product.urls')),
    path('api/', include('basket.urls')),
    path('api/', include('order.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
