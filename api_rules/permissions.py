from rest_framework import permissions
from api_rules.models import PermissionRow
from django.core.cache import cache
from desk.model import Desk, Column, Comment, Task
from debug.db_queries import DbQueries
LOCAL_DEBUG_SQL = False

permission_dict = {
    "STAFF": 1,
    "EDITOR": 2,
    "ADMIN": 3
}


def check_base_permission(request, view, permission, weight):
    """
    @request: Request object
    @view: View object
    @permission: ADMIN/EDITOR/STAFF
    @weight: weight of the role(1, 2, 3)
    This one checks if user has permission to create column/task/comment for desk with id='kwargs['desk_id']'
    """
    print("Works......")
    dict = request.parser_context.get('kwargs')
    print(cache.get(request.user.id))
    # If DESK object is requested else return True
    if 'desk_id' in dict.keys():

        # Check if user's data is in cache.         
        if cache.get(request.user.id) is None:
            return False
        
        # If user's permission is in cache 
        # TODO: Think about this one validation
        if dict['desk_id'] in cache.get(request.user.id).keys():
            desk_role = cache.get(request.user.id)[dict['desk_id']]
            return permission_dict[desk_role] > weight
        else: 
            return False
    else:
        return True


class IsAdminOfDesk(permissions.BasePermission):
    """
    Only author of the Desk object is ADMIN
    """

    def has_permission(self, request, view):
        return check_base_permission(request, view, "ADMIN", 2)

        
    def has_object_permission(self, request, view, obj):
        return request.user == obj.desk_author


class IsEditorOfDeskOrHigher(permissions.BasePermission):
    """
    EDITOR user has the same permissions as ADMIN but cannot edit ADMIN role and DELETE Desk(weight: 2)
    """
    def has_permission(self, request, view):

        return check_base_permission(request, view, "EDITOR", 1)

    def has_object_permission(self, request, view, obj):
        #print(cache.get(request.user.id))
        user_perms = cache.get(request.user.id)
        #perm = user_perms[]
        print(request.parser_context.get('kwargs'))
        return True
        # if isinstance(obj, PermissionRow):
        #         user_set = PermissionRow.objects.prefetch_related("user")\
        #             .filter(related_desk=obj.related_desk, user=request.user).first()
        #
        # if isinstance(obj, Desk):
        #     user_set = obj.permissionrow_set.filter(user=request.user).first()
        #
        # if isinstance(obj, Column):
        #     user_set = obj.related_desk.permissionrow_set.filter(user=request.user).first()
        #
        # if isinstance(obj, Task):
        #
        #     # If task is assigned to this user then he can edit it regardless from permission
        #     if request.user == obj.current_executor:
        #         return True
        #
        #     user_set = obj.related_column.related_desk.permissionrow_set.filter(user=request.user).first()
        #
        # if isinstance(obj, Comment):
        #     user_set = obj.related_task.related_column.related_desk.permissionrow_set.filter(user=request.user).first()

        if user_set is not None:
            return permission_dict[user_set.permission] > 1

        return False


class IsStaffOfDeskOrHigher(permissions.BasePermission):
    """
    STAFF user has minimal permissions (weight: 1)
    """
    def has_permission(self, request, view):

        return check_base_permission(request, view, "STAFF", 0)

    def has_object_permission(self, request, view, obj):

        user_set = None

        if isinstance(obj, PermissionRow):
                user_set = PermissionRow.objects.prefetch_related("user")\
                    .filter(related_desk=obj.related_desk, user=request.user).first()

        if isinstance(obj, Desk):
            user_set = obj.permissionrow_set.filter(user=request.user).first()

        if isinstance(obj, Column):
            user_set = obj.related_desk.permissionrow_set.filter(user=request.user).first()

        if isinstance(obj, Task):
            user_set = obj.related_column.related_desk.permissionrow_set.filter(user=request.user).first()

        if isinstance(obj, Comment):
            user_set = obj.related_task.related_column.related_desk.permissionrow_set.filter(user=request.user).first()

        if user_set is not None:
            return permission_dict[user_set.permission] > 0

        return False
