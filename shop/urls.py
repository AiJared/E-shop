from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

API_TITLE = "E-shop"
API_DESCRIPTION = "E-shop is an Ecommerce application API."


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include_docs_urls(title=API_TITLE,
                                description=API_DESCRIPTION
                                )),
    path("api/v1/", include("api.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, documet_root=settings.MEDIA_ROOT)
