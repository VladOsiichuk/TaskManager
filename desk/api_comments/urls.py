from django.urls import path, include
from .views import CommentAPIView, CreateCommentAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("comments/", csrf_exempt(CommentAPIView.as_view())),
    path("comments/create/", csrf_exempt(CreateCommentAPIView.as_view()))
]
