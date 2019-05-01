from django.conf.urls import url
from .views import (ColumnAPIView,
                    ColumnDetailAPIView)
from django.urls import path, include


urlpatterns = [
    path("columns/", ColumnAPIView.as_view()),
    path("columns/<int:column_id>/", ColumnDetailAPIView.as_view()),
    path("columns/<int:column_id>/", include("desk.api_tasks.urls")),
]
