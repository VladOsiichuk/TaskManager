from django.conf.urls import url
from .views import (DeskAPIView,
                    DeskDetailAPIView)
from django.urls import path, include
from api_rules.views import SetUsersPermissionsAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', DeskAPIView.as_view()),
    path('<int:desk_id>/', csrf_exempt(DeskDetailAPIView.as_view())),
    path('<int:desk_id>/', include("api_rules.urls")),
    path("<int:desk_id>/", include("desk.api_columns.urls")),
]
