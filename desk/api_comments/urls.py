from django.urls import path, include
from .views import CommentAPIView, CreateCommentAPIView

urlpatterns = [
    path("comments/", CommentAPIView.as_view()),
    path("comments/create/", CreateCommentAPIView.as_view())
]
