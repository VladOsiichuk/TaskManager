from django.urls import path, include
from .views import TaskAPIView, TaskDetailAPIView


urlpatterns = [
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/<int:task_id>/', TaskDetailAPIView.as_view()),
    path("tasks/<int:task_id>/", include('desk.api_comments.urls')),
]
