from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('django-admin/', admin.site.urls),

]

urlpatterns += i18n_patterns(
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('main.urls')),
    path('news/', include('news.urls', namespace="news")),
    path('services/', include('services.urls', namespace="services")),
    path('library/', include('library.urls', namespace="library")),
    path('store/', include('store.urls', namespace="store")),
    path('cart/', include('cart.urls', namespace="cart")),
    path('wishlist/', include('wishlist.urls', namespace="wishlist")),
    path('checkout/', include('checkout.urls', namespace="checkout")),
    path('orders/', include('orders.urls', namespace="orders")),
    path('admin/', include('administration.urls', namespace="administration")),

    path('api/', include('api.urls', 'api')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^languages/', include('rosetta.urls'))
    ]
