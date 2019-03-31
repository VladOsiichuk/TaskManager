from django.conf.urls import url
from .views import (DeskAPIView,
                    DeskDetailAPIView)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_rules.views import SetUsersPermissionsAPIView
from desk.api_columns.views import ColumnAPIView, ColumnDetailAPIView

urlpatterns = [
    path('<int:id>/', DeskDetailAPIView.as_view()),
    path('', DeskAPIView.as_view()),
    path('<int:id>/rules/', SetUsersPermissionsAPIView.as_view()),
    path('<int:id>/columns/', ColumnAPIView.as_view()),
    path('<int:id>/columns/<int:pk>/', ColumnDetailAPIView.as_view()),
]
