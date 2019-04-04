from django.urls import path, include
from .views import SetUsersPermissionsAPIView, UpdateUsersPermissionsAPIView

urlpatterns = [
    path("rules/", SetUsersPermissionsAPIView.as_view()),
    path("rules/update/", UpdateUsersPermissionsAPIView.as_view()),
]
