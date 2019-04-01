from django.conf.urls import url
from .views import (DeskAPIView,
                    DeskDetailAPIView)
from django.urls import path, include
from api_rules.views import SetUsersPermissionsAPIView
# from desk.api_columns.views import ColumnAPIView, ColumnDetailAPIView
# from desk.api_tasks.views import TaskAPIView, TaskDetailAPIView
# from desk.api_comments.views import CommentAPIView

urlpatterns = [
    path('', DeskAPIView.as_view()),
    path('<int:desk_id>/', DeskDetailAPIView.as_view()),
    path('<int:desk_id>/rules/', SetUsersPermissionsAPIView.as_view()),
    path("<int:desk_id>/", include("desk.api_columns.urls")),
    # path('<int:desk_id>/columns/', ColumnAPIView.as_view()),
    # path('<int:desk_id>/columns/<int:column_id>/', ColumnDetailAPIView.as_view()),
    # path('<int:desk_id>/columns/<int:column_id>/tasks/', TaskAPIView.as_view()),
    # path('<int:desk_id>/columns/<int:column_id>/tasks/<int:task_id>/', TaskDetailAPIView.as_view()),
    # path('<int:desk_id>/columns/<int:column_id>/tasks/<int:task_id>/comments/',
    #      CommentAPIView.as_view()),

]
