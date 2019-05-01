from django.urls import path, include
from .views import TaskAPIView, TaskDetailAPIView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('tasks/', csrf_exempt(TaskAPIView.as_view())),
    path('tasks/<int:task_id>/', csrf_exempt(TaskDetailAPIView.as_view())),
    path("tasks/<int:task_id>/", include('desk.api_comments.urls')),
]
