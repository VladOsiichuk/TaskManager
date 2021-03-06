"""TaskManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
#from desk.api_desks.views import DeskDetailApiView, DeskModelListApiView


#router = routers.DefaultRouter()
#router.register(r'user', UserViewSet)



urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='API documentation', public=False)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-users/', include('user_auth.urls')),
    path('api-desks/', include('desk.api_desks.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),


        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
