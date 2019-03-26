from django.conf.urls import url
from .views import DeskDetailApiView, DeskModelListApiView
from django.urls import path

urlpatterns = [
    path('<int:id>/', DeskDetailApiView.as_view(), name="desk-detail"),
    url('', DeskModelListApiView.as_view(), name="desk-list"),

]
