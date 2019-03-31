from django.conf.urls import url
from .views import (ColumnAPIView,
                    ColumnDetailAPIView)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_rules.views import SetUsersPermissionsAPIView


urlpatterns = [
    path('<int:id>/', ColumnDetailAPIView.as_view()),
    path('', ColumnAPIView.as_view()),
]
