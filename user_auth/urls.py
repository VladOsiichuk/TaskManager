from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import UserRegisterAPIView, AuthView

#router = routers.DefaultRouter()
#router.register(r'user', UserViewSet)


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', AuthView.as_view()),
]
