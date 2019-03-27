from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import UserRegisterAPIView

#router = routers.DefaultRouter()
#router.register(r'user', UserViewSet)


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    #url('api_desks/', include('desk.api_desks.urls')),
]
