from django.conf.urls import url
from .views import (ColumnAPIView,
                    ColumnDetailAPIView)
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("columns/", csrf_exempt(ColumnAPIView.as_view())),
    path("columns/<int:column_id>/", csrf_exempt(ColumnDetailAPIView.as_view())),
    path("columns/<int:column_id>/", include("desk.api_tasks.urls")),
]
