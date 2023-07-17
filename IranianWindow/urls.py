from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/panel/', include('panel.urls', namespace='panel'),),
    path('', include_docs_urls(
                                title='Site APIs Document',
                                description='description of all APIs will add here', 
                            )
    )
]
