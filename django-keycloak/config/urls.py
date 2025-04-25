from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')), 
     # mozilla가 제공하는 keycloak 관련 엔드포인트 사용
    path('oidc/', include('mozilla_django_oidc.urls')),
]