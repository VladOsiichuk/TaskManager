from rest_framework import permissions
from api_rules.models import PermissionRow
from django.core.cache import cache
from desk.model import Desk, Column, Comment, Task
from debug.db_queries import DbQueries
from redis_manager.permission_cache_manager import PermissionCacheManager
from debug.db_queries import DbQueries
LOCAL_DEBUG_SQL = True

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

    dict = request.parser_context.get('kwargs')

    user_perms = PermissionCacheManager.get_user_perms(user_id=request.user.id)

    # If DESK object is requested else return True
    if 'desk_id' in dict.keys():
        
        # If user's permission is in cache 
        if dict['desk_id'] in user_perms.keys():
            desk_role = user_perms[dict['desk_id']]
            return permission_dict[desk_role] > weight
        else: 
            return False
    
    else:
        print("IS NOT DENIED")
        return True


class IsAdminOfDesk(permissions.BasePermission):
    """
    Only author of the Desk object is ADMIN
    """

    def has_permission(self, request, view):
        return check_base_permission(request, view, "ADMIN", 2)
 
    def has_object_permission(self, request, view, obj):
        return check_base_permission(request, view, "ADMIN", 2)


class IsEditorOfDeskOrHigher(permissions.BasePermission):
    """
    EDITOR user has the same permissions as ADMIN but cannot edit ADMIN role and DELETE Desk(weight: 2)
    """

    def has_permission(self, request, view):
        return check_base_permission(request, view, "EDITOR", 1)

    def has_object_permission(self, request, view, obj):
        
        # asignee can always change tasks
        if isinstance(obj, Task):
            if obj.current_executor == request.user:
                return True
        
        return check_base_permission(request, view, "EDITOR", 1)


class IsStaffOfDeskOrHigher(permissions.BasePermission):
    """
    STAFF user has minimal permissions (weight: 1)
    """
    
    def has_permission(self, request, view):
        return check_base_permission(request, view, "STAFF", 0)

    def has_object_permission(self, request, view, obj):
        return check_base_permission(request, view, "STAFF", 0)
