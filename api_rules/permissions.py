from rest_framework import permissions
from desk.model import Desk, Column, Comment, Task


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

    def has_object_permission(self, request, view, obj):

        user_set = None

        if isinstance(obj, Desk):
            user_set = obj.permissionrow_set.all()

        if isinstance(obj, Column):
            user_set = obj.related_desk.permissionrow_set.all()

        if isinstance(obj, Task):

            # If task is assigned to this user then he can edit it regardless from permission
            if request.user == obj.current_executor:
                return True

            user_set = obj.related_column.related_desk.permissionrow_set.all()

        if isinstance(obj, Comment):
            user_set = obj.related_task.related_column.related_desk.permissionrow_set.all()

        user_perm = user_set.filter(user=request.user).first()
        if user_perm:
            return permission_dict[user_perm.permission] > 1

        return False


class IsStaffOfDeskOrHigher(permissions.BasePermission):
    """
    STAFF user has minimal permissions (weight: 1)
    """

    def has_object_permission(self, request, view, obj):
        user_set = None
        print(obj)
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
