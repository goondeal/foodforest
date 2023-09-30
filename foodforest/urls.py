from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # restaurants
    path('api/v1/restaurants/', include('restaurants.urls')),

    # orders
    path('api/v1/orders/', include('orders.urls')),

    # management
    path('api/v1/management/', include('management.urls')),


    # authentication
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),

    # admin
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
