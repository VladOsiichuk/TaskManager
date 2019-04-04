from django.urls import path, include
from .views import UserRegisterAPIView, AuthView, UserAPIView
from django.contrib.auth import views


urlpatterns = [
    path('<int:id>/', UserAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', AuthView.as_view()),
    path('logout/', views.LogoutView.as_view())

]
