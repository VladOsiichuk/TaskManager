from django.urls import path, include
from .views import CommentAPIView

urlpatterns = [
    path("comments/", CommentAPIView.as_view())
]
