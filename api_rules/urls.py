from django.conf.urls import url
from .views import AddUserWithPermissionsAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'desks', DeskModelListApiView, base_name='all_desks')
# router.register('desk', DeskDetailApiView, base_name='desk')
#

urlpatterns = [
    #path('create/', DeskCreateAPIView.as_view()),
    #path('<int:id>/', DeskDetailAPIView.as_view()),
    # path('<int:id>/update', DeskUpdateAPIView.as_view()),
    # path('<int:id>/delete', DeskDeleteAPIView.as_view()),
    path('<int:id>/', AddUserWithPermissionsAPIView.as_view()),
]
