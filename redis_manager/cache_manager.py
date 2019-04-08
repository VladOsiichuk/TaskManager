from django.core.cache import cache
from api_rules.models import PermissionRow
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

class CacheManager:
    """
    In cache we store data related to the permissions of users. data can be get using ID of user key
    """
    ttl = settings.CACHE_TTL

    @classmethod
    def get_user_perms(self, user_id):
        """
        returns data about all user's perms in dict = {"desk_id": "permission", "desk2_id:...."} or None if does not exists
        """

        id = self._get_user_id(user_id)

        if id is None:
            return None

        user_perms = cache.get(id)
        
        if user_perms is not None:
            return user_perms
        else:
            return self.set_user_perms_in_cache(id)

    @classmethod
    def _get_user_id(self, user_id):
        """
        check if user_id is int object else return None
        """
        if not isinstance(user_id, int):
            return None
        return user_id
    
    @classmethod
    def set_user_perms_in_cache(self, user_id):
        """
        set cache with user's permissions. Structure of data in cache: '[user_id]: {dict of values with key=desk_id and value=permission}' 
        """

        id = self._get_user_id(user_id)
        if id is None:
            return None
        
        permissions = PermissionRow.objects.filter(user_id=user_id)

        # cache permissions
        permission_dict = {perm.related_desk_id: perm.permission for perm in permissions}

        cache.set(id, permission_dict, self.ttl*60)

        return cache.get(id)
    
    @classmethod
    def update_cache_of_user(self, user_id, permission, desk_id):
        data = cache.get(user_id)
        
        if data is not None:
            data.update({desk_id: permission})
            cache.set(user_id, data)

    @classmethod
    def delete_user_cache_row(self, user_id, desk_id):
        """ Use this method if you want to delete one permission row in the cache """

        user_info = cache.get(user_id)
        del user_info[desk_id]
        cache.set(user_id, user_info)