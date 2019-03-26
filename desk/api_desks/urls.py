from django.conf.urls import url
from .views import DeskDetailApiView, DeskModelListApiView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'desks', DeskModelListApiView, base_name='all_desks')
router.register('desk', DeskDetailApiView, base_name='desk')


urlpatterns = [
    path('', include(router.urls)),
    #    path('<int:id>/', DeskDetailApiView),
#    url('', DeskModelListApiView),

]
