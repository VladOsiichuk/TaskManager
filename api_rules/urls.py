from django.urls import path, include
from .views import SetUsersPermissionsAPIView, UpdateUsersPermissionsAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("rules/", csrf_exempt(SetUsersPermissionsAPIView.as_view())),
    path("rules/update/", csrf_exempt(UpdateUsersPermissionsAPIView.as_view())),
]
