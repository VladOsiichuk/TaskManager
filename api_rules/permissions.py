from rest_framework import permissions
#from user_auth.models import CustomGroup
from .models import PermissionRow
from desk.model import Desk, Column, Comment, Task


permission_dict = {
    "STAFF": 1,
    "EDITOR": 2,
    "ADMIN": 3
}


class IsAdminOfDesk(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     print(type(view))
    #     print(view)
    #     desk = Desk.objects.get(id=self.kwargs["id"])
    #
    #     return desk.author == request.user

    """
    Only author of the Desk object is ADMIN
    """
    def has_object_permission(self, request, view, obj):
        print(type(obj))
        return request.user == obj.desk_author


class IsEditorOfDeskOrHigher(permissions.BasePermission):
    """
    EDITOR user should be in the EDITOR_desk.name_desk.id CustomGroup
    """

    def has_object_permission(self, request, view, obj):

        # # check if user not ADMIN
        # if request.user == obj.desk_author:
        #     return True
        #
        # group_name = "EDITOR_" + obj.desk_name + "_" + str(obj.desk_id)
        #
        # return request.user in CustomGroup.objects.get(name=group_name).user_set.all()
        user_set = None

        if isinstance(obj, Desk):
            user_set = obj.permissionrow_set.all()

        if isinstance(obj, Column):
            user_set = obj.related_desk.permissionrow_set.all()

        if isinstance(obj, Task):
            user_set = obj.related_column.related_desk.permissionrow_set.all()

        if isinstance(obj, Comment):
            user_set = obj.related_task.related_column.related_desk.permissionrow_set.all()

        #print(user_set)
        user_perm = user_set.filter(user=request.user).first()
        if user_perm:
            return permission_dict[user_perm.permission] > 1

        return False


class IsStaffOfDeskOrHigher(permissions.BasePermission):
    """
    STAFF user should be in the STAFF_desk.name_desk.id CustomGroup
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

    #class IsParticipantOfDesk(permissions.BasePermission):
    """
    check if user is participant of this desk
    """

#    def has_object_permission(self, request, view, obj):

#        group_name = "COMMON_" + obj.desk_name + "_" + str(obj.desk_id)

#        return request.user in CustomGroup.objects.get(name=group_name).user_set.all()
