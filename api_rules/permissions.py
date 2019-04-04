from django.views import View
from rest_framework import permissions
from rest_framework.request import Request
from api_rules.models import PermissionRow

from desk.model import Desk, Column, Comment, Task
from debug.db_queries import DbQueries
LOCAL_DEBUG_SQL = False

permission_dict = {
    "STAFF": 1,
    "EDITOR": 2,
    "ADMIN": 3
}


class IsAdminOfDesk(permissions.BasePermission):
    """
    Only author of the Desk object is ADMIN
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.desk_author


class IsEditorOfDeskOrHigher(permissions.BasePermission):
    """
    EDITOR user has the same permissions as ADMIN but cannot edit ADMIN role(weight: 2)
    """

    def has_permission(self, request: Request, view: View) -> bool:
        #DbQueries.show(l_dbg_sql=LOCAL_DEBUG_SQL)
        return True

    def has_object_permission(self, request, view, obj):
        print("CHECKING PERMISSIONS")
        DbQueries.show(l_dbg_sql=LOCAL_DEBUG_SQL)
        user_set = None

        if isinstance(obj, PermissionRow):

                user_set = PermissionRow.objects.prefetch_related("user")\
                    .filter(related_desk=obj.related_desk, user=request.user).first()

        if isinstance(obj, Desk):
            try:
                print(type(request.user))
                user_set = obj.permissionrow_set.filter(user=request.user).first()
                print(user_set, type(user_set))
            except PermissionRow.DoesNotExist:
                return False

        if isinstance(obj, Column):

            user_set = obj.related_desk.permissionrow_set.filter(user=request.user).first()

        if isinstance(obj, Task):

            # If task is assigned to this user then he can edit it regardless from permission
            if request.user == obj.current_executor:
                return True

            user_set = obj.related_column.related_desk.permissionrow_set.filter(user=request.user).first()

        if isinstance(obj, Comment):
            user_set = obj.related_task.related_column.related_desk.permissionrow_set.all()

        if user_set is not None:
            return permission_dict[user_set.permission] > 1

        return False


class IsStaffOfDeskOrHigher(permissions.BasePermission):
    """
    STAFF user has minimal permissions (weight: 1)
    """

    def has_object_permission(self, request, view, obj):

        user_set = None

        if isinstance(obj, PermissionRow):
                user_set = PermissionRow.objects.prefetch_related("user")\
                    .filter(related_desk=obj.related_desk, user=request.user).first()

        if isinstance(obj, Desk):
            user_set = obj.permissionrow_set.all()

        if isinstance(obj, Column):
            user_set = obj.related_desk.permissionrow_set.all()

        if isinstance(obj, Task):
            user_set = obj.related_column.related_desk.permissionrow_set.all()

        if isinstance(obj, Comment):
            user_set = obj.related_task.related_column.related_desk.permissionrow_set.all()

        # print(user_set)
        user_perm = user_set.filter(user=request.user).first()
        if user_perm:
            return permission_dict[user_perm.permission] > 0

        return False
