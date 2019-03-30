from rest_framework import permissions
#from user_auth.models import CustomGroup
from .models import PermissionRow
from desk.model import Desk

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
        print(type(obj))
        return request.user == obj.desk_author


class IsEditorOfDeskOrHigher(permissions.BasePermission):
    """
    EDITOR user should be in the EDITOR_desk.name_desk.id CustomGroup
    """
    #def has_permission(self, request, view):
        #return False

    def has_object_permission(self, request, view, obj):

        # # check if user not ADMIN
        # if request.user == obj.desk_author:
        #     return True
        #
        # group_name = "EDITOR_" + obj.desk_name + "_" + str(obj.desk_id)
        #
        # return request.user in CustomGroup.objects.get(name=group_name).user_set.all()

        user_set = obj.permissionrow_set.all()
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

        return False
        # check if user is not ADMIN
        # if request.user == obj.desk_author:
        #     return True
        #
        # # check if user is not EDITOR
        # editor_group_name = "EDITOR_" + obj.desk_name + "_" + str(obj.desk_id)
        # if request.user in CustomGroup.objects.get(name=editor_group_name).user_set.all():
        #     return True
        #
        # group_name = "STAFF_" + obj.desk_name + "_" + str(obj.desk_id)
        #
        # return request.user in CustomGroup.objects.get(name=group_name).user_set.all()


#class IsParticipantOfDesk(permissions.BasePermission):
    """
    check if user is participant of this desk
    """

#    def has_object_permission(self, request, view, obj):

#        group_name = "COMMON_" + obj.desk_name + "_" + str(obj.desk_id)

#        return request.user in CustomGroup.objects.get(name=group_name).user_set.all()
