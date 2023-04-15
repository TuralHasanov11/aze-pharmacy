from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('main.urls')),
    path('news/', include('news.urls', namespace="news")),
    path('services/', include('services.urls', namespace="services")),
    path('library/', include('library.urls', namespace="library")),
    path('store/', include('store.urls', namespace="store")),
    path('cart/', include('cart.urls', namespace="cart")),
    path('checkout/', include('checkout.urls', namespace="checkout")),
    path('admin/', include('administration.urls', namespace="administration"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
