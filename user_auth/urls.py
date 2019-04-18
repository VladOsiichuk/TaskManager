from django.urls import path, include
from .views import UserRegisterAPIView, AuthAPIView, UserAPIView, LogoutAPIView
from django.contrib.auth import views


urlpatterns = [
    path('<int:id>/', UserAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', AuthAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view())
]
