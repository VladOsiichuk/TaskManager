from django.core.cache import cache
from django.conf import settings


class PermissionCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:

            user_id = request.user.id
            ttl = settings.CACHE_TTL
            
            # refresh user's cache 
            cache.expire(user_id, timeout=ttl*60)

            response = self.get_response(request)

        else:
            response = self.get_response(request)
        print(response)
        return response
